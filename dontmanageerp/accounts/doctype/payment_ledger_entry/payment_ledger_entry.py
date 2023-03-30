# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from dontmanageerp.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_checks_for_pl_and_bs_accounts,
)
from dontmanageerp.accounts.doctype.accounting_dimension_filter.accounting_dimension_filter import (
	get_dimension_filter_map,
)
from dontmanageerp.accounts.doctype.gl_entry.gl_entry import (
	validate_balance_type,
	validate_frozen_account,
)
from dontmanageerp.accounts.utils import update_voucher_outstanding
from dontmanageerp.exceptions import InvalidAccountDimensionError, MandatoryAccountDimensionError


class PaymentLedgerEntry(Document):
	def validate_account(self):
		valid_account = dontmanage.db.get_list(
			"Account",
			"name",
			filters={"name": self.account, "account_type": self.account_type, "company": self.company},
			ignore_permissions=True,
		)
		if not valid_account:
			dontmanage.throw(_("{0} account is not of type {1}").format(self.account, self.account_type))

	def validate_account_details(self):
		"""Account must be ledger, active and not freezed"""

		ret = dontmanage.db.sql(
			"""select is_group, docstatus, company
			from tabAccount where name=%s""",
			self.account,
			as_dict=1,
		)[0]

		if ret.is_group == 1:
			dontmanage.throw(
				_(
					"""{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions"""
				).format(self.voucher_type, self.voucher_no, self.account)
			)

		if ret.docstatus == 2:
			dontmanage.throw(
				_("{0} {1}: Account {2} is inactive").format(self.voucher_type, self.voucher_no, self.account)
			)

		if ret.company != self.company:
			dontmanage.throw(
				_("{0} {1}: Account {2} does not belong to Company {3}").format(
					self.voucher_type, self.voucher_no, self.account, self.company
				)
			)

	def validate_allowed_dimensions(self):
		dimension_filter_map = get_dimension_filter_map()
		for key, value in dimension_filter_map.items():
			dimension = key[0]
			account = key[1]

			if self.account == account:
				if value["is_mandatory"] and not self.get(dimension):
					dontmanage.throw(
						_("{0} is mandatory for account {1}").format(
							dontmanage.bold(dontmanage.unscrub(dimension)), dontmanage.bold(self.account)
						),
						MandatoryAccountDimensionError,
					)

				if value["allow_or_restrict"] == "Allow":
					if self.get(dimension) and self.get(dimension) not in value["allowed_dimensions"]:
						dontmanage.throw(
							_("Invalid value {0} for {1} against account {2}").format(
								dontmanage.bold(self.get(dimension)),
								dontmanage.bold(dontmanage.unscrub(dimension)),
								dontmanage.bold(self.account),
							),
							InvalidAccountDimensionError,
						)
				else:
					if self.get(dimension) and self.get(dimension) in value["allowed_dimensions"]:
						dontmanage.throw(
							_("Invalid value {0} for {1} against account {2}").format(
								dontmanage.bold(self.get(dimension)),
								dontmanage.bold(dontmanage.unscrub(dimension)),
								dontmanage.bold(self.account),
							),
							InvalidAccountDimensionError,
						)

	def validate_dimensions_for_pl_and_bs(self):
		account_type = dontmanage.db.get_value("Account", self.account, "report_type")

		for dimension in get_checks_for_pl_and_bs_accounts():
			if (
				account_type == "Profit and Loss"
				and self.company == dimension.company
				and dimension.mandatory_for_pl
				and not dimension.disabled
			):
				if not self.get(dimension.fieldname):
					dontmanage.throw(
						_("Accounting Dimension <b>{0}</b> is required for 'Profit and Loss' account {1}.").format(
							dimension.label, self.account
						)
					)

			if (
				account_type == "Balance Sheet"
				and self.company == dimension.company
				and dimension.mandatory_for_bs
				and not dimension.disabled
			):
				if not self.get(dimension.fieldname):
					dontmanage.throw(
						_("Accounting Dimension <b>{0}</b> is required for 'Balance Sheet' account {1}.").format(
							dimension.label, self.account
						)
					)

	def validate(self):
		self.validate_account()

	def on_update(self):
		adv_adj = self.flags.adv_adj
		if not self.flags.from_repost:
			self.validate_account_details()
			self.validate_dimensions_for_pl_and_bs()
			self.validate_allowed_dimensions()
			validate_balance_type(self.account, adv_adj)
			validate_frozen_account(self.account, adv_adj)

		# update outstanding amount
		if (
			self.against_voucher_type in ["Journal Entry", "Sales Invoice", "Purchase Invoice", "Fees"]
			and self.flags.update_outstanding == "Yes"
			and not dontmanage.flags.is_reverse_depr_entry
		):
			update_voucher_outstanding(
				self.against_voucher_type, self.against_voucher_no, self.account, self.party_type, self.party
			)


def on_doctype_update():
	dontmanage.db.add_index("Payment Ledger Entry", ["against_voucher_no", "against_voucher_type"])
	dontmanage.db.add_index("Payment Ledger Entry", ["voucher_no", "voucher_type"])
