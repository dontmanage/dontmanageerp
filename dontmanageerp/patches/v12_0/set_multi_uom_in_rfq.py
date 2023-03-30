# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("buying", "doctype", "request_for_quotation_item")

	dontmanage.db.sql(
		"""UPDATE `tabRequest for Quotation Item`
			SET
				stock_uom = uom,
				conversion_factor = 1,
				stock_qty = qty"""
	)
