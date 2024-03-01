# Copyright (c) 2023, DontManage and Contributors
# See license.txt

import dontmanage
from dontmanage import qb
from dontmanage.query_builder.functions import Sum
from dontmanage.tests.utils import DontManageTestCase, change_settings
from dontmanage.utils import add_days, nowdate, today

from dontmanageerp.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from dontmanageerp.accounts.doctype.payment_request.payment_request import make_payment_request
from dontmanageerp.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import start_repost
from dontmanageerp.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from dontmanageerp.accounts.test.accounts_mixin import AccountsTestMixin
from dontmanageerp.accounts.utils import get_fiscal_year


class TestRepostAccountingLedger(AccountsTestMixin, DontManageTestCase):
	def setUp(self):
		self.create_company()
		self.create_customer()
		self.create_item()
		update_repost_settings()

	def tearDown(self):
		dontmanage.db.rollback()

	def test_01_basic_functions(self):
		si = create_sales_invoice(
			item=self.item,
			company=self.company,
			customer=self.customer,
			debit_to=self.debit_to,
			parent_cost_center=self.cost_center,
			cost_center=self.cost_center,
			rate=100,
		)

		preq = dontmanage.get_doc(
			make_payment_request(
				dt=si.doctype,
				dn=si.name,
				payment_request_type="Inward",
				party_type="Customer",
				party=si.customer,
			)
		)
		preq.save().submit()

		# Test Validation Error
		ral = dontmanage.new_doc("Repost Accounting Ledger")
		ral.company = self.company
		ral.delete_cancelled_entries = True
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append(
			"vouchers", {"voucher_type": preq.doctype, "voucher_no": preq.name}
		)  # this should throw validation error
		self.assertRaises(dontmanage.ValidationError, ral.save)
		ral.vouchers.pop()
		preq.cancel()
		preq.delete()

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save()

		# manually set an incorrect debit amount in DB
		gle = dontmanage.db.get_all("GL Entry", filters={"voucher_no": si.name, "account": self.debit_to})
		dontmanage.db.set_value("GL Entry", gle[0], "debit", 90)

		gl = qb.DocType("GL Entry")
		res = (
			qb.from_(gl)
			.select(gl.voucher_no, Sum(gl.debit).as_("debit"), Sum(gl.credit).as_("credit"))
			.where((gl.voucher_no == si.name) & (gl.is_cancelled == 0))
			.run()
		)

		# Assert incorrect ledger balance
		self.assertNotEqual(res[0], (si.name, 100, 100))

		# Submit repost document
		ral.save().submit()

		res = (
			qb.from_(gl)
			.select(gl.voucher_no, Sum(gl.debit).as_("debit"), Sum(gl.credit).as_("credit"))
			.where((gl.voucher_no == si.name) & (gl.is_cancelled == 0))
			.run()
		)

		# Ledger should reflect correct amount post repost
		self.assertEqual(res[0], (si.name, 100, 100))

	def test_02_deferred_accounting_valiations(self):
		si = create_sales_invoice(
			item=self.item,
			company=self.company,
			customer=self.customer,
			debit_to=self.debit_to,
			parent_cost_center=self.cost_center,
			cost_center=self.cost_center,
			rate=100,
			do_not_submit=True,
		)
		si.items[0].enable_deferred_revenue = True
		si.items[0].deferred_revenue_account = self.deferred_revenue
		si.items[0].service_start_date = nowdate()
		si.items[0].service_end_date = add_days(nowdate(), 90)
		si.save().submit()

		ral = dontmanage.new_doc("Repost Accounting Ledger")
		ral.company = self.company
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		self.assertRaises(dontmanage.ValidationError, ral.save)

	@change_settings("Accounts Settings", {"delete_linked_ledger_entries": 1})
	def test_04_pcv_validation(self):
		# Clear old GL entries so PCV can be submitted.
		gl = dontmanage.qb.DocType("GL Entry")
		qb.from_(gl).delete().where(gl.company == self.company).run()

		si = create_sales_invoice(
			item=self.item,
			company=self.company,
			customer=self.customer,
			debit_to=self.debit_to,
			parent_cost_center=self.cost_center,
			cost_center=self.cost_center,
			rate=100,
		)
		pcv = dontmanage.get_doc(
			{
				"doctype": "Period Closing Voucher",
				"transaction_date": today(),
				"posting_date": today(),
				"company": self.company,
				"fiscal_year": get_fiscal_year(today(), company=self.company)[0],
				"cost_center": self.cost_center,
				"closing_account_head": self.retained_earnings,
				"remarks": "test",
			}
		)
		pcv.save().submit()

		ral = dontmanage.new_doc("Repost Accounting Ledger")
		ral.company = self.company
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		self.assertRaises(dontmanage.ValidationError, ral.save)

		pcv.reload()
		pcv.cancel()
		pcv.delete()

	def test_03_deletion_flag_and_preview_function(self):
		si = create_sales_invoice(
			item=self.item,
			company=self.company,
			customer=self.customer,
			debit_to=self.debit_to,
			parent_cost_center=self.cost_center,
			cost_center=self.cost_center,
			rate=100,
		)

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()

		# with deletion flag set
		ral = dontmanage.new_doc("Repost Accounting Ledger")
		ral.company = self.company
		ral.delete_cancelled_entries = True
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save().submit()

		self.assertIsNone(dontmanage.db.exists("GL Entry", {"voucher_no": si.name, "is_cancelled": 1}))
		self.assertIsNone(dontmanage.db.exists("GL Entry", {"voucher_no": pe.name, "is_cancelled": 1}))

	def test_05_without_deletion_flag(self):
		si = create_sales_invoice(
			item=self.item,
			company=self.company,
			customer=self.customer,
			debit_to=self.debit_to,
			parent_cost_center=self.cost_center,
			cost_center=self.cost_center,
			rate=100,
		)

		pe = get_payment_entry(si.doctype, si.name)
		pe.save().submit()

		# without deletion flag set
		ral = dontmanage.new_doc("Repost Accounting Ledger")
		ral.company = self.company
		ral.delete_cancelled_entries = False
		ral.append("vouchers", {"voucher_type": si.doctype, "voucher_no": si.name})
		ral.append("vouchers", {"voucher_type": pe.doctype, "voucher_no": pe.name})
		ral.save().submit()

		self.assertIsNotNone(dontmanage.db.exists("GL Entry", {"voucher_no": si.name, "is_cancelled": 1}))
		self.assertIsNotNone(dontmanage.db.exists("GL Entry", {"voucher_no": pe.name, "is_cancelled": 1}))


def update_repost_settings():
	allowed_types = ["Sales Invoice", "Purchase Invoice", "Payment Entry", "Journal Entry"]
	repost_settings = dontmanage.get_doc("Repost Accounting Ledger Settings")
	for x in allowed_types:
		repost_settings.append("allowed_types", {"document_type": x, "allowed": True})
		repost_settings.save()
