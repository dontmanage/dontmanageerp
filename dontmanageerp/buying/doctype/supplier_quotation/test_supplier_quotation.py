# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestPurchaseOrder(DontManageTestCase):
	def test_make_purchase_order(self):
		from dontmanageerp.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order

		sq = dontmanage.copy_doc(test_records[0]).insert()

		self.assertRaises(dontmanage.ValidationError, make_purchase_order, sq.name)

		sq = dontmanage.get_doc("Supplier Quotation", sq.name)
		sq.submit()
		po = make_purchase_order(sq.name)

		self.assertEqual(po.doctype, "Purchase Order")
		self.assertEqual(len(po.get("items")), len(sq.get("items")))

		po.naming_series = "_T-Purchase Order-"

		for doc in po.get("items"):
			if doc.get("item_code"):
				doc.set("schedule_date", "2013-04-12")

		po.insert()


test_records = dontmanage.get_test_records("Supplier Quotation")
