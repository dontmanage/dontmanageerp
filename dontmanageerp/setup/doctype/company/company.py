# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import json

import dontmanage
import dontmanage.defaults
from dontmanage import _
from dontmanage.cache_manager import clear_defaults_cache
from dontmanage.contacts.address_and_contact import load_address_and_contact
from dontmanage.custom.doctype.property_setter.property_setter import make_property_setter
from dontmanage.desk.page.setup_wizard.setup_wizard import make_records
from dontmanage.utils import cint, formatdate, get_timestamp, today
from dontmanage.utils.nestedset import NestedSet, rebuild_tree

from dontmanageerp.accounts.doctype.account.account import get_account_currency
from dontmanageerp.setup.setup_wizard.operations.taxes_setup import setup_taxes_and_charges


class Company(NestedSet):
	nsm_parent_field = "parent_company"

	def onload(self):
		load_address_and_contact(self, "company")

	@dontmanage.whitelist()
	def check_if_transactions_exist(self):
		exists = False
		for doctype in [
			"Sales Invoice",
			"Delivery Note",
			"Sales Order",
			"Quotation",
			"Purchase Invoice",
			"Purchase Receipt",
			"Purchase Order",
			"Supplier Quotation",
		]:
			if dontmanage.db.sql(
				"""select name from `tab%s` where company=%s and docstatus=1
					limit 1"""
				% (doctype, "%s"),
				self.name,
			):
				exists = True
				break

		return exists

	def validate(self):
		self.update_default_account = False
		if self.is_new():
			self.update_default_account = True

		self.validate_abbr()
		self.validate_default_accounts()
		self.validate_currency()
		self.validate_coa_input()
		self.validate_perpetual_inventory()
		self.validate_provisional_account_for_non_stock_items()
		self.check_country_change()
		self.check_parent_changed()
		self.set_chart_of_accounts()
		self.validate_parent_company()

	def validate_abbr(self):
		if not self.abbr:
			self.abbr = "".join(c[0] for c in self.company_name.split()).upper()

		self.abbr = self.abbr.strip()

		if not self.abbr.strip():
			dontmanage.throw(_("Abbreviation is mandatory"))

		if dontmanage.db.sql(
			"select abbr from tabCompany where name!=%s and abbr=%s", (self.name, self.abbr)
		):
			dontmanage.throw(_("Abbreviation already used for another company"))

	@dontmanage.whitelist()
	def create_default_tax_template(self):
		setup_taxes_and_charges(self.name, self.country)

	def validate_default_accounts(self):
		accounts = [
			["Default Bank Account", "default_bank_account"],
			["Default Cash Account", "default_cash_account"],
			["Default Receivable Account", "default_receivable_account"],
			["Default Payable Account", "default_payable_account"],
			["Default Expense Account", "default_expense_account"],
			["Default Income Account", "default_income_account"],
			["Stock Received But Not Billed Account", "stock_received_but_not_billed"],
			["Stock Adjustment Account", "stock_adjustment_account"],
			["Expense Included In Valuation Account", "expenses_included_in_valuation"],
		]

		for account in accounts:
			if self.get(account[1]):
				for_company = dontmanage.db.get_value("Account", self.get(account[1]), "company")
				if for_company != self.name:
					dontmanage.throw(
						_("Account {0} does not belong to company: {1}").format(self.get(account[1]), self.name)
					)

				if get_account_currency(self.get(account[1])) != self.default_currency:
					error_message = _(
						"{0} currency must be same as company's default currency. Please select another account."
					).format(dontmanage.bold(account[0]))
					dontmanage.throw(error_message)

	def validate_currency(self):
		if self.is_new():
			return
		self.previous_default_currency = dontmanage.get_cached_value(
			"Company", self.name, "default_currency"
		)
		if (
			self.default_currency
			and self.previous_default_currency
			and self.default_currency != self.previous_default_currency
			and self.check_if_transactions_exist()
		):
			dontmanage.throw(
				_(
					"Cannot change company's default currency, because there are existing transactions. Transactions must be cancelled to change the default currency."
				)
			)

	def on_update(self):
		NestedSet.on_update(self)
		if not dontmanage.db.sql(
			"""select name from tabAccount
				where company=%s and docstatus<2 limit 1""",
			self.name,
		):
			if not dontmanage.local.flags.ignore_chart_of_accounts:
				dontmanage.flags.country_change = True
				self.create_default_accounts()
				self.create_default_warehouses()

		if not dontmanage.db.get_value("Cost Center", {"is_group": 0, "company": self.name}):
			self.create_default_cost_center()

		if dontmanage.flags.country_change:
			install_country_fixtures(self.name, self.country)
			self.create_default_tax_template()

		if not dontmanage.db.get_value("Department", {"company": self.name}):
			self.create_default_departments()

		if not dontmanage.local.flags.ignore_chart_of_accounts:
			self.set_default_accounts()
			if self.default_cash_account:
				self.set_mode_of_payment_account()

		if self.default_currency:
			dontmanage.db.set_value("Currency", self.default_currency, "enabled", 1)

		if (
			hasattr(dontmanage.local, "enable_perpetual_inventory")
			and self.name in dontmanage.local.enable_perpetual_inventory
		):
			dontmanage.local.enable_perpetual_inventory[self.name] = self.enable_perpetual_inventory

		if dontmanage.flags.parent_company_changed:
			from dontmanage.utils.nestedset import rebuild_tree

			rebuild_tree("Company", "parent_company")

		dontmanage.clear_cache()

	def create_default_warehouses(self):
		for wh_detail in [
			{"warehouse_name": _("All Warehouses"), "is_group": 1},
			{"warehouse_name": _("Stores"), "is_group": 0},
			{"warehouse_name": _("Work In Progress"), "is_group": 0},
			{"warehouse_name": _("Finished Goods"), "is_group": 0},
			{"warehouse_name": _("Goods In Transit"), "is_group": 0, "warehouse_type": "Transit"},
		]:

			if not dontmanage.db.exists(
				"Warehouse", "{0} - {1}".format(wh_detail["warehouse_name"], self.abbr)
			):
				warehouse = dontmanage.get_doc(
					{
						"doctype": "Warehouse",
						"warehouse_name": wh_detail["warehouse_name"],
						"is_group": wh_detail["is_group"],
						"company": self.name,
						"parent_warehouse": "{0} - {1}".format(_("All Warehouses"), self.abbr)
						if not wh_detail["is_group"]
						else "",
						"warehouse_type": wh_detail["warehouse_type"] if "warehouse_type" in wh_detail else None,
					}
				)
				warehouse.flags.ignore_permissions = True
				warehouse.flags.ignore_mandatory = True
				warehouse.insert()

	def create_default_accounts(self):
		from dontmanageerp.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts

		dontmanage.local.flags.ignore_root_company_validation = True
		create_charts(self.name, self.chart_of_accounts, self.existing_company)

		self.db_set(
			"default_receivable_account",
			dontmanage.db.get_value(
				"Account", {"company": self.name, "account_type": "Receivable", "is_group": 0}
			),
		)

		self.db_set(
			"default_payable_account",
			dontmanage.db.get_value(
				"Account", {"company": self.name, "account_type": "Payable", "is_group": 0}
			),
		)

	def create_default_departments(self):
		records = [
			# Department
			{
				"doctype": "Department",
				"department_name": _("All Departments"),
				"is_group": 1,
				"parent_department": "",
				"__condition": lambda: not dontmanage.db.exists("Department", _("All Departments")),
			},
			{
				"doctype": "Department",
				"department_name": _("Accounts"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Marketing"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Sales"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Purchase"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Operations"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Production"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Dispatch"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Customer Service"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Human Resources"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Management"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Quality Management"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Research & Development"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
			{
				"doctype": "Department",
				"department_name": _("Legal"),
				"parent_department": _("All Departments"),
				"company": self.name,
			},
		]

		# Make root department with NSM updation
		make_records(records[:1])

		dontmanage.local.flags.ignore_update_nsm = True
		make_records(records)
		dontmanage.local.flags.ignore_update_nsm = False
		rebuild_tree("Department", "parent_department")

	def validate_coa_input(self):
		if self.create_chart_of_accounts_based_on == "Existing Company":
			self.chart_of_accounts = None
			if not self.existing_company:
				dontmanage.throw(_("Please select Existing Company for creating Chart of Accounts"))

		else:
			self.existing_company = None
			self.create_chart_of_accounts_based_on = "Standard Template"
			if not self.chart_of_accounts:
				self.chart_of_accounts = "Standard"

	def validate_perpetual_inventory(self):
		if not self.get("__islocal"):
			if cint(self.enable_perpetual_inventory) == 1 and not self.default_inventory_account:
				dontmanage.msgprint(
					_("Set default inventory account for perpetual inventory"), alert=True, indicator="orange"
				)

	def validate_provisional_account_for_non_stock_items(self):
		if not self.get("__islocal"):
			if (
				cint(self.enable_provisional_accounting_for_non_stock_items) == 1
				and not self.default_provisional_account
			):
				dontmanage.throw(
					_("Set default {0} account for non stock items").format(dontmanage.bold("Provisional Account"))
				)

			make_property_setter(
				"Purchase Receipt",
				"provisional_expense_account",
				"hidden",
				not self.enable_provisional_accounting_for_non_stock_items,
				"Check",
				validate_fields_for_doctype=False,
			)

	def check_country_change(self):
		dontmanage.flags.country_change = False

		if not self.is_new() and self.country != dontmanage.get_cached_value(
			"Company", self.name, "country"
		):
			dontmanage.flags.country_change = True

	def set_chart_of_accounts(self):
		"""If parent company is set, chart of accounts will be based on that company"""
		if self.parent_company:
			self.create_chart_of_accounts_based_on = "Existing Company"
			self.existing_company = self.parent_company

	def validate_parent_company(self):
		if self.parent_company:
			is_group = dontmanage.get_value("Company", self.parent_company, "is_group")

			if not is_group:
				dontmanage.throw(_("Parent Company must be a group company"))

	def set_default_accounts(self):
		default_accounts = {
			"default_cash_account": "Cash",
			"default_bank_account": "Bank",
			"round_off_account": "Round Off",
			"accumulated_depreciation_account": "Accumulated Depreciation",
			"depreciation_expense_account": "Depreciation",
			"capital_work_in_progress_account": "Capital Work in Progress",
			"asset_received_but_not_billed": "Asset Received But Not Billed",
			"expenses_included_in_asset_valuation": "Expenses Included In Asset Valuation",
			"default_expense_account": "Cost of Goods Sold",
		}

		if self.enable_perpetual_inventory:
			default_accounts.update(
				{
					"stock_received_but_not_billed": "Stock Received But Not Billed",
					"default_inventory_account": "Stock",
					"stock_adjustment_account": "Stock Adjustment",
					"expenses_included_in_valuation": "Expenses Included In Valuation",
				}
			)

		if self.update_default_account:
			for default_account in default_accounts:
				self._set_default_account(default_account, default_accounts.get(default_account))

		if not self.default_income_account:
			income_account = dontmanage.db.get_value(
				"Account", {"account_name": _("Sales"), "company": self.name, "is_group": 0}
			)

			if not income_account:
				income_account = dontmanage.db.get_value(
					"Account", {"account_name": _("Sales Account"), "company": self.name}
				)

			self.db_set("default_income_account", income_account)

		if not self.default_payable_account:
			self.db_set("default_payable_account", self.default_payable_account)

		if not self.write_off_account:
			write_off_acct = dontmanage.db.get_value(
				"Account", {"account_name": _("Write Off"), "company": self.name, "is_group": 0}
			)

			self.db_set("write_off_account", write_off_acct)

		if not self.exchange_gain_loss_account:
			exchange_gain_loss_acct = dontmanage.db.get_value(
				"Account", {"account_name": _("Exchange Gain/Loss"), "company": self.name, "is_group": 0}
			)

			self.db_set("exchange_gain_loss_account", exchange_gain_loss_acct)

		if not self.disposal_account:
			disposal_acct = dontmanage.db.get_value(
				"Account",
				{"account_name": _("Gain/Loss on Asset Disposal"), "company": self.name, "is_group": 0},
			)

			self.db_set("disposal_account", disposal_acct)

	def _set_default_account(self, fieldname, account_type):
		if self.get(fieldname):
			return

		account = dontmanage.db.get_value(
			"Account", {"account_type": account_type, "is_group": 0, "company": self.name}
		)

		if account:
			self.db_set(fieldname, account)

	def set_mode_of_payment_account(self):
		cash = dontmanage.db.get_value("Mode of Payment", {"type": "Cash"}, "name")
		if (
			cash
			and self.default_cash_account
			and not dontmanage.db.get_value("Mode of Payment Account", {"company": self.name, "parent": cash})
		):
			mode_of_payment = dontmanage.get_doc("Mode of Payment", cash, for_update=True)
			mode_of_payment.append(
				"accounts", {"company": self.name, "default_account": self.default_cash_account}
			)
			mode_of_payment.save(ignore_permissions=True)

	def create_default_cost_center(self):
		cc_list = [
			{
				"cost_center_name": self.name,
				"company": self.name,
				"is_group": 1,
				"parent_cost_center": None,
			},
			{
				"cost_center_name": _("Main"),
				"company": self.name,
				"is_group": 0,
				"parent_cost_center": self.name + " - " + self.abbr,
			},
		]
		for cc in cc_list:
			cc.update({"doctype": "Cost Center"})
			cc_doc = dontmanage.get_doc(cc)
			cc_doc.flags.ignore_permissions = True

			if cc.get("cost_center_name") == self.name:
				cc_doc.flags.ignore_mandatory = True
			cc_doc.insert()

		self.db_set("cost_center", _("Main") + " - " + self.abbr)
		self.db_set("round_off_cost_center", _("Main") + " - " + self.abbr)
		self.db_set("depreciation_cost_center", _("Main") + " - " + self.abbr)

	def after_rename(self, olddn, newdn, merge=False):
		self.db_set("company_name", newdn)

		dontmanage.db.sql(
			"""update `tabDefaultValue` set defvalue=%s
			where defkey='Company' and defvalue=%s""",
			(newdn, olddn),
		)

		clear_defaults_cache()

	def abbreviate(self):
		self.abbr = "".join(c[0].upper() for c in self.company_name.split())

	def on_trash(self):
		"""
		Trash accounts and cost centers for this company if no gl entry exists
		"""
		NestedSet.validate_if_child_exists(self)
		dontmanage.utils.nestedset.update_nsm(self)

		rec = dontmanage.db.sql("SELECT name from `tabGL Entry` where company = %s", self.name)
		if not rec:
			dontmanage.db.sql(
				"""delete from `tabBudget Account`
				where exists(select name from tabBudget
					where name=`tabBudget Account`.parent and company = %s)""",
				self.name,
			)

			for doctype in ["Account", "Cost Center", "Budget", "Party Account"]:
				dontmanage.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		if not dontmanage.db.get_value("Stock Ledger Entry", {"company": self.name}):
			dontmanage.db.sql("""delete from `tabWarehouse` where company=%s""", self.name)

		dontmanage.defaults.clear_default("company", value=self.name)
		for doctype in ["Mode of Payment Account", "Item Default"]:
			dontmanage.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		# clear default accounts, warehouses from item
		warehouses = dontmanage.db.sql_list("select name from tabWarehouse where company=%s", self.name)
		if warehouses:
			dontmanage.db.sql(
				"""delete from `tabItem Reorder` where warehouse in (%s)"""
				% ", ".join(["%s"] * len(warehouses)),
				tuple(warehouses),
			)

		# reset default company
		dontmanage.db.sql(
			"""update `tabSingles` set value=''
			where doctype='Global Defaults' and field='default_company'
			and value=%s""",
			self.name,
		)

		# reset default company
		dontmanage.db.sql(
			"""update `tabSingles` set value=''
			where doctype='Chart of Accounts Importer' and field='company'
			and value=%s""",
			self.name,
		)

		# delete BOMs
		boms = dontmanage.db.sql_list("select name from tabBOM where company=%s", self.name)
		if boms:
			dontmanage.db.sql("delete from tabBOM where company=%s", self.name)
			for dt in ("BOM Operation", "BOM Item", "BOM Scrap Item", "BOM Explosion Item"):
				dontmanage.db.sql(
					"delete from `tab%s` where parent in (%s)" "" % (dt, ", ".join(["%s"] * len(boms))),
					tuple(boms),
				)

		dontmanage.db.sql("delete from tabEmployee where company=%s", self.name)
		dontmanage.db.sql("delete from tabDepartment where company=%s", self.name)
		dontmanage.db.sql("delete from `tabTax Withholding Account` where company=%s", self.name)
		dontmanage.db.sql("delete from `tabTransaction Deletion Record` where company=%s", self.name)

		# delete tax templates
		dontmanage.db.sql("delete from `tabSales Taxes and Charges Template` where company=%s", self.name)
		dontmanage.db.sql("delete from `tabPurchase Taxes and Charges Template` where company=%s", self.name)
		dontmanage.db.sql("delete from `tabItem Tax Template` where company=%s", self.name)

		# delete Process Deferred Accounts if no GL Entry found
		if not dontmanage.db.get_value("GL Entry", {"company": self.name}):
			dontmanage.db.sql("delete from `tabProcess Deferred Accounting` where company=%s", self.name)

	def check_parent_changed(self):
		dontmanage.flags.parent_company_changed = False

		if not self.is_new() and self.parent_company != dontmanage.db.get_value(
			"Company", self.name, "parent_company"
		):
			dontmanage.flags.parent_company_changed = True


def get_name_with_abbr(name, company):
	company_abbr = dontmanage.get_cached_value("Company", company, "abbr")
	parts = name.split(" - ")

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)


def install_country_fixtures(company, country):
	try:
		module_name = f"dontmanageerp.regional.{dontmanage.scrub(country)}.setup.setup"
		dontmanage.get_attr(module_name)(company, False)
	except ImportError:
		pass
	except Exception:
		dontmanage.log_error("Unable to set country fixtures")
		dontmanage.throw(
			_("Failed to setup defaults for country {0}. Please contact support.").format(
				dontmanage.bold(country)
			)
		)


def update_company_current_month_sales(company):
	current_month_year = formatdate(today(), "MM-yyyy")

	results = dontmanage.db.sql(
		"""
		SELECT
			SUM(base_grand_total) AS total,
			DATE_FORMAT(`posting_date`, '%m-%Y') AS month_year
		FROM
			`tabSales Invoice`
		WHERE
			DATE_FORMAT(`posting_date`, '%m-%Y') = '{current_month_year}'
			AND docstatus = 1
			AND company = {company}
		GROUP BY
			month_year
	""".format(
			current_month_year=current_month_year, company=dontmanage.db.escape(company)
		),
		as_dict=True,
	)

	monthly_total = results[0]["total"] if len(results) > 0 else 0

	dontmanage.db.set_value("Company", company, "total_monthly_sales", monthly_total)


def update_company_monthly_sales(company):
	"""Cache past year monthly sales of every company based on sales invoices"""
	import json

	from dontmanage.utils.goal import get_monthly_results

	filter_str = "company = {0} and status != 'Draft' and docstatus=1".format(
		dontmanage.db.escape(company)
	)
	month_to_value_dict = get_monthly_results(
		"Sales Invoice", "base_grand_total", "posting_date", filter_str, "sum"
	)

	dontmanage.db.set_value("Company", company, "sales_monthly_history", json.dumps(month_to_value_dict))


def update_transactions_annual_history(company, commit=False):
	transactions_history = get_all_transactions_annual_history(company)
	dontmanage.db.set_value(
		"Company", company, "transactions_annual_history", json.dumps(transactions_history)
	)

	if commit:
		dontmanage.db.commit()


def cache_companies_monthly_sales_history():
	companies = [d["name"] for d in dontmanage.get_list("Company")]
	for company in companies:
		update_company_monthly_sales(company)
		update_transactions_annual_history(company)
	dontmanage.db.commit()


@dontmanage.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	if parent == None or parent == "All Companies":
		parent = ""

	return dontmanage.db.sql(
		"""
		select
			name as value,
			is_group as expandable
		from
			`tabCompany` comp
		where
			ifnull(parent_company, "")={parent}
		""".format(
			parent=dontmanage.db.escape(parent)
		),
		as_dict=1,
	)


@dontmanage.whitelist()
def add_node():
	from dontmanage.desk.treeview import make_tree_args

	args = dontmanage.form_dict
	args = make_tree_args(**args)

	if args.parent_company == "All Companies":
		args.parent_company = None

	dontmanage.get_doc(args).insert()


def get_all_transactions_annual_history(company):
	out = {}

	items = dontmanage.db.sql(
		"""
		select transaction_date, count(*) as count

		from (
			select name, transaction_date, company
			from `tabQuotation`

			UNION ALL

			select name, transaction_date, company
			from `tabSales Order`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabDelivery Note`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabSales Invoice`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabIssue`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabProject`
		) t

		where
			company=%s
			and
			transaction_date > date_sub(curdate(), interval 1 year)

		group by
			transaction_date
			""",
		(company),
		as_dict=True,
	)

	for d in items:
		timestamp = get_timestamp(d["transaction_date"])
		out.update({timestamp: d["count"]})

	return out


def get_timeline_data(doctype, name):
	"""returns timeline data based on linked records in dashboard"""
	out = {}
	date_to_value_dict = {}

	history = dontmanage.get_cached_value("Company", name, "transactions_annual_history")

	try:
		date_to_value_dict = json.loads(history) if history and "{" in history else None
	except ValueError:
		date_to_value_dict = None

	if date_to_value_dict is None:
		update_transactions_annual_history(name, True)
		history = dontmanage.get_cached_value("Company", name, "transactions_annual_history")
		return json.loads(history) if history and "{" in history else {}

	return date_to_value_dict


@dontmanage.whitelist()
def get_default_company_address(name, sort_key="is_primary_address", existing_address=None):
	if sort_key not in ["is_shipping_address", "is_primary_address"]:
		return None

	out = dontmanage.db.sql(
		""" SELECT
			addr.name, addr.%s
		FROM
			`tabAddress` addr, `tabDynamic Link` dl
		WHERE
			dl.parent = addr.name and dl.link_doctype = 'Company' and
			dl.link_name = %s and ifnull(addr.disabled, 0) = 0
		"""
		% (sort_key, "%s"),
		(name),
	)  # nosec

	if existing_address:
		if existing_address in [d[0] for d in out]:
			return existing_address

	if out:
		return max(out, key=lambda x: x[1])[0]  # find max by sort_key
	else:
		return None


@dontmanage.whitelist()
def create_transaction_deletion_request(company):
	tdr = dontmanage.get_doc({"doctype": "Transaction Deletion Record", "company": company})
	tdr.insert()
	tdr.submit()
