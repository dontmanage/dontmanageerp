# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("stock", "doctype", "item_barcode")
	if dontmanage.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in dontmanage.db.get_table_columns("Item"):
		return

	items_barcode = dontmanage.db.sql(
		"select name, barcode from tabItem where barcode is not null", as_dict=True
	)
	dontmanage.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				dontmanage.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (dontmanage.DuplicateEntryError, dontmanage.UniqueValidationError):
				continue
