# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import cint, get_link_to_form


class AssetCategory(Document):
	def validate(self):
		self.validate_finance_books()
		self.validate_account_types()
		self.validate_account_currency()
		self.valide_cwip_account()

	def validate_finance_books(self):
		for d in self.finance_books:
			for field in ("Total Number of Depreciations", "Frequency of Depreciation"):
				if cint(d.get(dontmanage.scrub(field))) < 1:
					dontmanage.throw(
						_("Row {0}: {1} must be greater than 0").format(d.idx, field), dontmanage.MandatoryError
					)

	def validate_account_currency(self):
		account_types = [
			"fixed_asset_account",
			"accumulated_depreciation_account",
			"depreciation_expense_account",
			"capital_work_in_progress_account",
		]
		invalid_accounts = []
		for d in self.accounts:
			company_currency = dontmanage.get_value("Company", d.get("company_name"), "default_currency")
			for type_of_account in account_types:
				if d.get(type_of_account):
					account_currency = dontmanage.get_value("Account", d.get(type_of_account), "account_currency")
					if account_currency != company_currency:
						invalid_accounts.append(
							dontmanage._dict({"type": type_of_account, "idx": d.idx, "account": d.get(type_of_account)})
						)

		for d in invalid_accounts:
			dontmanage.throw(
				_("Row #{}: Currency of {} - {} doesn't matches company currency.").format(
					d.idx, dontmanage.bold(dontmanage.unscrub(d.type)), dontmanage.bold(d.account)
				),
				title=_("Invalid Account"),
			)

	def validate_account_types(self):
		account_type_map = {
			"fixed_asset_account": {"account_type": ["Fixed Asset"]},
			"accumulated_depreciation_account": {"account_type": ["Accumulated Depreciation"]},
			"depreciation_expense_account": {"root_type": ["Expense", "Income"]},
			"capital_work_in_progress_account": {"account_type": ["Capital Work in Progress"]},
		}
		for d in self.accounts:
			for fieldname in account_type_map.keys():
				if d.get(fieldname):
					selected_account = d.get(fieldname)
					key_to_match = next(iter(account_type_map.get(fieldname)))  # acount_type or root_type
					selected_key_type = dontmanage.db.get_value("Account", selected_account, key_to_match)
					expected_key_types = account_type_map[fieldname][key_to_match]

					if selected_key_type not in expected_key_types:
						dontmanage.throw(
							_(
								"Row #{}: {} of {} should be {}. Please modify the account or select a different account."
							).format(
								d.idx,
								dontmanage.unscrub(key_to_match),
								dontmanage.bold(selected_account),
								dontmanage.bold(expected_key_types),
							),
							title=_("Invalid Account"),
						)

	def valide_cwip_account(self):
		if self.enable_cwip_accounting:
			missing_cwip_accounts_for_company = []
			for d in self.accounts:
				if not d.capital_work_in_progress_account and not dontmanage.db.get_value(
					"Company", d.company_name, "capital_work_in_progress_account"
				):
					missing_cwip_accounts_for_company.append(get_link_to_form("Company", d.company_name))

			if missing_cwip_accounts_for_company:
				msg = _("""To enable Capital Work in Progress Accounting,""") + " "
				msg += _("""you must select Capital Work in Progress Account in accounts table""")
				msg += "<br><br>"
				msg += _("You can also set default CWIP account in Company {}").format(
					", ".join(missing_cwip_accounts_for_company)
				)
				dontmanage.throw(msg, title=_("Missing Account"))


@dontmanage.whitelist()
def get_asset_category_account(
	fieldname, item=None, asset=None, account=None, asset_category=None, company=None
):
	if item and dontmanage.db.get_value("Item", item, "is_fixed_asset"):
		asset_category = dontmanage.db.get_value("Item", item, ["asset_category"])

	elif not asset_category or not company:
		if account:
			if dontmanage.db.get_value("Account", account, "account_type") != "Fixed Asset":
				account = None

		if not account:
			asset_details = dontmanage.db.get_value("Asset", asset, ["asset_category", "company"])
			asset_category, company = asset_details or [None, None]

	account = dontmanage.db.get_value(
		"Asset Category Account",
		filters={"parent": asset_category, "company_name": company},
		fieldname=fieldname,
	)

	return account
