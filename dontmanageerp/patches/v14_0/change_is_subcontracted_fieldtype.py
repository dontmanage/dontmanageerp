# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		dontmanage.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null"""
		)
		dontmanage.db.sql(
			f"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'"""
		)

		dontmanage.reload_doc(dontmanage.get_meta(doctype).module, "doctype", dontmanage.scrub(doctype))
