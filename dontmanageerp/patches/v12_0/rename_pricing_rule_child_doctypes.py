# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

doctypes = {
	"Price Discount Slab": "Promotional Scheme Price Discount",
	"Product Discount Slab": "Promotional Scheme Product Discount",
	"Apply Rule On Item Code": "Pricing Rule Item Code",
	"Apply Rule On Item Group": "Pricing Rule Item Group",
	"Apply Rule On Brand": "Pricing Rule Brand",
}


def execute():
	for old_doc, new_doc in doctypes.items():
		if not dontmanage.db.table_exists(new_doc) and dontmanage.db.table_exists(old_doc):
			dontmanage.rename_doc("DocType", old_doc, new_doc)
			dontmanage.reload_doc("accounts", "doctype", dontmanage.scrub(new_doc))
			dontmanage.delete_doc("DocType", old_doc)
