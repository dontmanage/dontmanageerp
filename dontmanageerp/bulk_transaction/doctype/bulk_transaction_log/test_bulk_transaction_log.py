# Copyright (c) 2021, DontManage and Contributors
# See license.txt

import unittest
from datetime import date

import dontmanage

from dontmanageerp.utilities.bulk_transaction import transaction_processing


class TestBulkTransactionLog(unittest.TestCase):
	def setUp(self):
		create_company()
		create_customer()
		create_item()

	def test_entry_in_log(self):
		so_name = create_so()
		transaction_processing([{"name": so_name}], "Sales Order", "Sales Invoice")
		doc = dontmanage.get_doc("Bulk Transaction Log", str(date.today()))
		for d in doc.get("logger_data"):
			if d.transaction_name == so_name:
				self.assertEqual(d.transaction_name, so_name)
				self.assertEqual(d.transaction_status, "Success")
				self.assertEqual(d.from_doctype, "Sales Order")
				self.assertEqual(d.to_doctype, "Sales Invoice")
				self.assertEqual(d.retried, 0)


def create_company():
	if not dontmanage.db.exists("Company", "_Test Company"):
		dontmanage.get_doc(
			{
				"doctype": "Company",
				"company_name": "_Test Company",
				"country": "India",
				"default_currency": "INR",
			}
		).insert()


def create_customer():
	if not dontmanage.db.exists("Customer", "Bulk Customer"):
		dontmanage.get_doc({"doctype": "Customer", "customer_name": "Bulk Customer"}).insert()


def create_item():
	if not dontmanage.db.exists("Item", "MK"):
		dontmanage.get_doc(
			{
				"doctype": "Item",
				"item_code": "MK",
				"item_name": "Milk",
				"description": "Milk",
				"item_group": "Products",
			}
		).insert()


def create_so(intent=None):
	so = dontmanage.new_doc("Sales Order")
	so.customer = "Bulk Customer"
	so.company = "_Test Company"
	so.transaction_date = date.today()

	so.set_warehouse = "Finished Goods - _TC"
	so.append(
		"items",
		{
			"item_code": "MK",
			"delivery_date": date.today(),
			"qty": 10,
			"rate": 80,
		},
	)
	so.insert()
	so.submit()
	return so.name
