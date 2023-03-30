# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice", "Supplier Quotation"]:
		dontmanage.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 0
				where is_subcontracted in ('', 'No') or is_subcontracted is null""".format(
				doctype=doctype
			)
		)
		dontmanage.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_subcontracted = 1
				where is_subcontracted = 'Yes'""".format(
				doctype=doctype
			)
		)

		dontmanage.reload_doc(dontmanage.get_meta(doctype).module, "doctype", dontmanage.scrub(doctype))
