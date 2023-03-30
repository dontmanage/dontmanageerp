# Copyright (c) 2018, DontManage and Contributors
# See license.txt

import unittest

import dontmanage


class TestCashFlowMapping(unittest.TestCase):
	def setUp(self):
		if dontmanage.db.exists("Cash Flow Mapping", "Test Mapping"):
			dontmanage.delete_doc("Cash Flow Mappping", "Test Mapping")

	def tearDown(self):
		dontmanage.delete_doc("Cash Flow Mapping", "Test Mapping")

	def test_multiple_selections_not_allowed(self):
		doc = dontmanage.new_doc("Cash Flow Mapping")
		doc.mapping_name = "Test Mapping"
		doc.label = "Test label"
		doc.append("accounts", {"account": "Accounts Receivable - _TC"})
		doc.is_working_capital = 1
		doc.is_finance_cost = 1

		self.assertRaises(dontmanage.ValidationError, doc.insert)

		doc.is_finance_cost = 0
		doc.insert()
