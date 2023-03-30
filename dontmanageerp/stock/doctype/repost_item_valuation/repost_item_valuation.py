# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.exceptions import QueryDeadlockError, QueryTimeoutError
from dontmanage.model.document import Document
from dontmanage.query_builder import DocType, Interval
from dontmanage.query_builder.functions import Now
from dontmanage.utils import cint, get_link_to_form, get_weekday, getdate, now, nowtime
from dontmanage.utils.user import get_users_with_role
from rq.timeouts import JobTimeoutException

import dontmanageerp
from dontmanageerp.accounts.utils import get_future_stock_vouchers, repost_gle_for_stock_vouchers
from dontmanageerp.stock.stock_ledger import (
	get_affected_transactions,
	get_items_to_be_repost,
	repost_future_sle,
)

RecoverableErrors = (JobTimeoutException, QueryDeadlockError, QueryTimeoutError)


class RepostItemValuation(Document):
	@staticmethod
	def clear_old_logs(days=None):
		days = days or 90
		table = DocType("Repost Item Valuation")
		dontmanage.db.delete(
			table,
			filters=(
				(table.modified < (Now() - Interval(days=days)))
				& (table.status.isin(["Completed", "Skipped"]))
			),
		)

	def validate(self):
		self.set_status(write=False)
		self.reset_field_values()
		self.set_company()
		self.validate_accounts_freeze()

	def validate_accounts_freeze(self):
		acc_settings = dontmanage.db.get_value(
			"Accounts Settings",
			"Accounts Settings",
			["acc_frozen_upto", "frozen_accounts_modifier"],
			as_dict=1,
		)
		if not acc_settings.acc_frozen_upto:
			return
		if getdate(self.posting_date) <= getdate(acc_settings.acc_frozen_upto):
			if (
				acc_settings.frozen_accounts_modifier
				and dontmanage.session.user in get_users_with_role(acc_settings.frozen_accounts_modifier)
			):
				dontmanage.msgprint(_("Caution: This might alter frozen accounts."))
				return
			dontmanage.throw(
				_("You cannot repost item valuation before {}").format(acc_settings.acc_frozen_upto)
			)

	def reset_field_values(self):
		if self.based_on == "Transaction":
			self.item_code = None
			self.warehouse = None

		self.allow_negative_stock = 1

	def set_company(self):
		if self.based_on == "Transaction":
			self.company = dontmanage.get_cached_value(self.voucher_type, self.voucher_no, "company")
		elif self.warehouse:
			self.company = dontmanage.get_cached_value("Warehouse", self.warehouse, "company")

	def set_status(self, status=None, write=True):
		status = status or self.status
		if not status:
			self.status = "Queued"
		else:
			self.status = status
		if write:
			self.db_set("status", self.status)

	def on_submit(self):
		"""During tests reposts are executed immediately.

		Exceptions:
		        1. "Repost Item Valuation" document has self.flags.dont_run_in_test
		        2. global flag dontmanage.flags.dont_execute_stock_reposts is set

		        These flags are useful for asserting real time behaviour like quantity updates.
		"""

		if not dontmanage.flags.in_test:
			return
		if self.flags.dont_run_in_test or dontmanage.flags.dont_execute_stock_reposts:
			return

		repost(self)

	def before_cancel(self):
		self.check_pending_repost_against_cancelled_transaction()

	def check_pending_repost_against_cancelled_transaction(self):
		if self.status not in ("Queued", "In Progress"):
			return

		if not (self.voucher_no and self.voucher_no):
			return

		transaction_status = dontmanage.db.get_value(self.voucher_type, self.voucher_no, "docstatus")
		if transaction_status == 2:
			msg = _("Cannot cancel as processing of cancelled documents is  pending.")
			msg += "<br>" + _("Please try again in an hour.")
			dontmanage.throw(msg, title=_("Pending processing"))

	@dontmanage.whitelist()
	def restart_reposting(self):
		self.set_status("Queued", write=False)
		self.current_index = 0
		self.distinct_item_and_warehouse = None
		self.items_to_be_repost = None
		self.gl_reposting_index = 0
		self.db_update()

	def deduplicate_similar_repost(self):
		"""Deduplicate similar reposts based on item-warehouse-posting combination."""
		if self.based_on != "Item and Warehouse":
			return

		filters = {
			"item_code": self.item_code,
			"warehouse": self.warehouse,
			"name": self.name,
			"posting_date": self.posting_date,
			"posting_time": self.posting_time,
		}

		dontmanage.db.sql(
			"""
			update `tabRepost Item Valuation`
			set status = 'Skipped'
			WHERE item_code = %(item_code)s
				and warehouse = %(warehouse)s
				and name != %(name)s
				and TIMESTAMP(posting_date, posting_time) > TIMESTAMP(%(posting_date)s, %(posting_time)s)
				and docstatus = 1
				and status = 'Queued'
				and based_on = 'Item and Warehouse'
				""",
			filters,
		)


def on_doctype_update():
	dontmanage.db.add_index("Repost Item Valuation", ["warehouse", "item_code"], "item_warehouse")


def repost(doc):
	try:
		if not dontmanage.db.exists("Repost Item Valuation", doc.name):
			return

		# This is to avoid TooManyWritesError in case of large reposts
		dontmanage.db.MAX_WRITES_PER_TRANSACTION *= 4

		doc.set_status("In Progress")
		if not dontmanage.flags.in_test:
			dontmanage.db.commit()

		repost_sl_entries(doc)
		repost_gl_entries(doc)

		doc.set_status("Completed")

	except Exception as e:
		if dontmanage.flags.in_test:
			# Don't silently fail in tests,
			# there is no reason for reposts to fail in CI
			raise

		dontmanage.db.rollback()
		traceback = dontmanage.get_traceback()
		doc.log_error("Unable to repost item valuation")

		message = dontmanage.message_log.pop() if dontmanage.message_log else ""
		if traceback:
			message += "<br>" + "Traceback: <br>" + traceback
		dontmanage.db.set_value(doc.doctype, doc.name, "error_log", message)

		if not isinstance(e, RecoverableErrors):
			notify_error_to_stock_managers(doc, message)
			doc.set_status("Failed")
	finally:
		if not dontmanage.flags.in_test:
			dontmanage.db.commit()


def repost_sl_entries(doc):
	if doc.based_on == "Transaction":
		repost_future_sle(
			voucher_type=doc.voucher_type,
			voucher_no=doc.voucher_no,
			allow_negative_stock=doc.allow_negative_stock,
			via_landed_cost_voucher=doc.via_landed_cost_voucher,
			doc=doc,
		)
	else:
		repost_future_sle(
			args=[
				dontmanage._dict(
					{
						"item_code": doc.item_code,
						"warehouse": doc.warehouse,
						"posting_date": doc.posting_date,
						"posting_time": doc.posting_time,
					}
				)
			],
			allow_negative_stock=doc.allow_negative_stock,
			via_landed_cost_voucher=doc.via_landed_cost_voucher,
			doc=doc,
		)


def repost_gl_entries(doc):
	if not cint(dontmanageerp.is_perpetual_inventory_enabled(doc.company)):
		return

	# directly modified transactions
	directly_dependent_transactions = _get_directly_dependent_vouchers(doc)
	repost_affected_transaction = get_affected_transactions(doc)
	repost_gle_for_stock_vouchers(
		directly_dependent_transactions + list(repost_affected_transaction),
		doc.posting_date,
		doc.company,
		repost_doc=doc,
	)


def _get_directly_dependent_vouchers(doc):
	"""Get stock vouchers that are directly affected by reposting
	i.e. any one item-warehouse is present in the stock transaction"""

	items = set()
	warehouses = set()

	if doc.based_on == "Transaction":
		ref_doc = dontmanage.get_doc(doc.voucher_type, doc.voucher_no)
		doc_items, doc_warehouses = ref_doc.get_items_and_warehouses()
		items.update(doc_items)
		warehouses.update(doc_warehouses)

		sles = get_items_to_be_repost(doc.voucher_type, doc.voucher_no)
		sle_items = {sle.item_code for sle in sles}
		sle_warehouses = {sle.warehouse for sle in sles}
		items.update(sle_items)
		warehouses.update(sle_warehouses)
	else:
		items.add(doc.item_code)
		warehouses.add(doc.warehouse)

	affected_vouchers = get_future_stock_vouchers(
		posting_date=doc.posting_date,
		posting_time=doc.posting_time,
		for_warehouses=list(warehouses),
		for_items=list(items),
		company=doc.company,
	)
	return affected_vouchers


def notify_error_to_stock_managers(doc, traceback):
	recipients = get_users_with_role("Stock Manager")
	if not recipients:
		recipients = get_users_with_role("System Manager")

	subject = _("Error while reposting item valuation")
	message = (
		_("Hi,")
		+ "<br>"
		+ _("An error has been appeared while reposting item valuation via {0}").format(
			get_link_to_form(doc.doctype, doc.name)
		)
		+ "<br>"
		+ _(
			"Please check the error message and take necessary actions to fix the error and then restart the reposting again."
		)
	)
	dontmanage.sendmail(recipients=recipients, subject=subject, message=message)


def repost_entries():
	"""
	Reposts 'Repost Item Valuation' entries in queue.
	Called hourly via hooks.py.
	"""
	if not in_configured_timeslot():
		return

	riv_entries = get_repost_item_valuation_entries()

	for row in riv_entries:
		doc = dontmanage.get_doc("Repost Item Valuation", row.name)
		if doc.status in ("Queued", "In Progress"):
			repost(doc)
			doc.deduplicate_similar_repost()

	riv_entries = get_repost_item_valuation_entries()
	if riv_entries:
		return


def get_repost_item_valuation_entries():
	return dontmanage.db.sql(
		""" SELECT name from `tabRepost Item Valuation`
		WHERE status in ('Queued', 'In Progress') and creation <= %s and docstatus = 1
		ORDER BY timestamp(posting_date, posting_time) asc, creation asc
	""",
		now(),
		as_dict=1,
	)


def in_configured_timeslot(repost_settings=None, current_time=None):
	"""Check if current time is in configured timeslot for reposting."""

	if repost_settings is None:
		repost_settings = dontmanage.get_cached_doc("Stock Reposting Settings")

	if not repost_settings.limit_reposting_timeslot:
		return True

	if get_weekday() == repost_settings.limits_dont_apply_on:
		return True

	start_time = repost_settings.start_time
	end_time = repost_settings.end_time

	now_time = current_time or nowtime()

	if start_time < end_time:
		return end_time >= now_time >= start_time
	else:
		return now_time >= start_time or now_time <= end_time


@dontmanage.whitelist()
def execute_repost_item_valuation():
	"""Execute repost item valuation via scheduler."""
	dontmanage.get_doc("Scheduled Job Type", "repost_item_valuation.repost_entries").enqueue(force=True)
