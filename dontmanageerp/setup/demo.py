# Copyright (c) 2023, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import json
import os
from random import randint

import dontmanage
from dontmanage import _
from dontmanage.utils import add_days, getdate

from dontmanageerp.accounts.doctype.payment_entry.payment_entry import get_payment_entry
from dontmanageerp.accounts.utils import get_fiscal_year
from dontmanageerp.buying.doctype.purchase_order.purchase_order import make_purchase_invoice
from dontmanageerp.selling.doctype.sales_order.sales_order import make_sales_invoice
from dontmanageerp.setup.setup_wizard.operations.install_fixtures import create_bank_account


def setup_demo_data():
	from dontmanage.utils.telemetry import capture

	capture("demo_data_creation_started", "dontmanageerp")
	try:
		company = create_demo_company()
		process_masters()
		make_transactions(company)
		dontmanage.cache.delete_keys("bootinfo")
		dontmanage.publish_realtime("demo_data_complete")
	except Exception:
		dontmanage.log_error("Failed to create demo data")
		capture("demo_data_creation_failed", "dontmanageerp", properties={"exception": dontmanage.get_traceback()})
		raise
	capture("demo_data_creation_completed", "dontmanageerp")


@dontmanage.whitelist()
def clear_demo_data():
	from dontmanage.utils.telemetry import capture

	dontmanage.only_for("System Manager")

	capture("demo_data_erased", "dontmanageerp")
	try:
		company = dontmanage.db.get_single_value("Global Defaults", "demo_company")
		create_transaction_deletion_record(company)
		clear_masters()
		delete_company(company)
		default_company = dontmanage.db.get_single_value("Global Defaults", "default_company")
		dontmanage.db.set_default("company", default_company)
	except Exception:
		dontmanage.db.rollback()
		dontmanage.log_error("Failed to erase demo data")
		dontmanage.throw(
			_("Failed to erase demo data, please delete the demo company manually."),
			title=_("Could Not Delete Demo Data"),
		)


def create_demo_company():
	company = dontmanage.db.get_all("Company")[0].name
	company_doc = dontmanage.get_doc("Company", company)

	# Make a dummy company
	new_company = dontmanage.new_doc("Company")
	new_company.company_name = company_doc.company_name + " (Demo)"
	new_company.abbr = company_doc.abbr + "D"
	new_company.enable_perpetual_inventory = 1
	new_company.default_currency = company_doc.default_currency
	new_company.country = company_doc.country
	new_company.chart_of_accounts_based_on = "Standard Template"
	new_company.chart_of_accounts = company_doc.chart_of_accounts
	new_company.insert()

	# Set Demo Company as default to
	dontmanage.db.set_single_value("Global Defaults", "demo_company", new_company.name)
	dontmanage.db.set_default("company", new_company.name)

	bank_account = create_bank_account({"company_name": new_company.name})
	dontmanage.db.set_value("Company", new_company.name, "default_bank_account", bank_account.name)

	return new_company.name


def process_masters():
	for doctype in dontmanage.get_hooks("demo_master_doctypes"):
		data = read_data_file_using_hooks(doctype)
		if data:
			for item in json.loads(data):
				create_demo_record(item)


def create_demo_record(doctype):
	dontmanage.get_doc(doctype).insert(ignore_permissions=True)


def make_transactions(company):
	dontmanage.db.set_single_value("Stock Settings", "allow_negative_stock", 1)
	from dontmanageerp.accounts.utils import FiscalYearError

	try:
		start_date = get_fiscal_year(date=getdate())[1]
	except FiscalYearError:
		# User might have setup fiscal year for previous or upcoming years
		active_fiscal_years = dontmanage.db.get_all("Fiscal Year", filters={"disabled": 0}, as_list=1)
		if active_fiscal_years:
			start_date = dontmanage.db.get_value("Fiscal Year", active_fiscal_years[0][0], "year_start_date")
		else:
			dontmanage.throw(_("There are no active Fiscal Years for which Demo Data can be generated."))

	for doctype in dontmanage.get_hooks("demo_transaction_doctypes"):
		data = read_data_file_using_hooks(doctype)
		if data:
			for item in json.loads(data):
				create_transaction(item, company, start_date)

	convert_order_to_invoices()
	dontmanage.db.set_single_value("Stock Settings", "allow_negative_stock", 0)


def create_transaction(doctype, company, start_date):
	document_type = doctype.get("doctype")
	warehouse = get_warehouse(company)

	if document_type == "Purchase Order":
		posting_date = get_random_date(start_date, 1, 25)
	else:
		posting_date = get_random_date(start_date, 31, 350)

	doctype.update(
		{
			"company": company,
			"set_posting_time": 1,
			"transaction_date": posting_date,
			"schedule_date": posting_date,
			"delivery_date": posting_date,
			"set_warehouse": warehouse,
		}
	)

	doc = dontmanage.get_doc(doctype)
	doc.save(ignore_permissions=True)
	doc.submit()


def convert_order_to_invoices():
	for document in ["Purchase Order", "Sales Order"]:
		# Keep some orders intentionally unbilled/unpaid
		for i, order in enumerate(
			dontmanage.db.get_all(
				document, filters={"docstatus": 1}, fields=["name", "transaction_date"], limit=6
			)
		):

			if document == "Purchase Order":
				invoice = make_purchase_invoice(order.name)
			elif document == "Sales Order":
				invoice = make_sales_invoice(order.name)

			invoice.set_posting_time = 1
			invoice.posting_date = order.transaction_date
			invoice.due_date = order.transaction_date
			invoice.bill_date = order.transaction_date

			if invoice.get("payment_schedule"):
				invoice.payment_schedule[0].due_date = order.transaction_date

			invoice.update_stock = 1
			invoice.submit()

			if i % 2 != 0:
				payment = get_payment_entry(invoice.doctype, invoice.name)
				payment.posting_date = order.transaction_date
				payment.reference_no = invoice.name
				payment.submit()


def get_random_date(start_date, start_range, end_range):
	return add_days(start_date, randint(start_range, end_range))


def create_transaction_deletion_record(company):
	transaction_deletion_record = dontmanage.new_doc("Transaction Deletion Record")
	transaction_deletion_record.company = company
	transaction_deletion_record.save(ignore_permissions=True)
	transaction_deletion_record.submit()


def clear_masters():
	for doctype in dontmanage.get_hooks("demo_master_doctypes")[::-1]:
		data = read_data_file_using_hooks(doctype)
		if data:
			for item in json.loads(data):
				clear_demo_record(item)


def clear_demo_record(document):
	document_type = document.get("doctype")
	del document["doctype"]

	valid_columns = dontmanage.get_meta(document_type).get_valid_columns()

	filters = document
	for key in list(filters):
		if key not in valid_columns:
			filters.pop(key, None)

	doc = dontmanage.get_doc(document_type, filters)
	doc.delete(ignore_permissions=True)


def delete_company(company):
	dontmanage.db.set_single_value("Global Defaults", "demo_company", "")
	dontmanage.delete_doc("Company", company, ignore_permissions=True)


def read_data_file_using_hooks(doctype):
	path = os.path.join(os.path.dirname(__file__), "demo_data")
	with open(os.path.join(path, doctype + ".json"), "r") as f:
		data = f.read()

	return data


def get_warehouse(company):
	warehouses = dontmanage.db.get_all("Warehouse", {"company": company, "is_group": 0})
	return warehouses[randint(0, 3)].name