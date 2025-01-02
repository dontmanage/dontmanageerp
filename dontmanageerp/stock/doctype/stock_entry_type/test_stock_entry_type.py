# Copyright (c) 2019, DontManage and Contributors
# See license.txt

import unittest

import dontmanage


class TestStockEntryType(unittest.TestCase):
	def test_stock_entry_type_non_standard(self):
		stock_entry_type = "Test Manufacturing"

		doc = dontmanage.get_doc(
			{
				"doctype": "Stock Entry Type",
				"__newname": stock_entry_type,
				"purpose": "Manufacture",
				"is_standard": 1,
			}
		)

		self.assertRaises(dontmanage.ValidationError, doc.insert)

	def test_stock_entry_type_is_standard(self):
		for stock_entry_type in [
			"Material Issue",
			"Material Receipt",
			"Material Transfer",
			"Material Transfer for Manufacture",
			"Material Consumption for Manufacture",
			"Manufacture",
			"Repack",
			"Send to Subcontractor",
		]:
			self.assertTrue(dontmanage.db.get_value("Stock Entry Type", stock_entry_type, "is_standard"))
