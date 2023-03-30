# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage

test_records = dontmanage.get_test_records("Product Bundle")


def make_product_bundle(parent, items, qty=None):
	if dontmanage.db.exists("Product Bundle", parent):
		return dontmanage.get_doc("Product Bundle", parent)

	product_bundle = dontmanage.get_doc({"doctype": "Product Bundle", "new_item_code": parent})

	for item in items:
		product_bundle.append("items", {"item_code": item, "qty": qty or 1})

	product_bundle.insert()

	return product_bundle
