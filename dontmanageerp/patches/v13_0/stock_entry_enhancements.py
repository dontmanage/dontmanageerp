# Copyright(c) 2020, DontManage Technologies Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("stock", "doctype", "stock_entry")
	if dontmanage.db.has_column("Stock Entry", "add_to_transit"):
		dontmanage.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		dontmanage.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		dontmanage.reload_doc("stock", "doctype", "warehouse_type")
		if not dontmanage.db.exists("Warehouse Type", "Transit"):
			doc = dontmanage.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		dontmanage.reload_doc("stock", "doctype", "stock_entry_type")
		dontmanage.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		dontmanage.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
