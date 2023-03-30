# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	"""`sales_invoice` field from loyalty point entry is splitted into `invoice_type` & `invoice` fields"""

	dontmanage.reload_doc("Accounts", "doctype", "loyalty_point_entry")

	if not dontmanage.db.has_column("Loyalty Point Entry", "sales_invoice"):
		return

	dontmanage.db.sql(
		"""UPDATE `tabLoyalty Point Entry` lpe
		SET lpe.`invoice_type` = 'Sales Invoice', lpe.`invoice` = lpe.`sales_invoice`
		WHERE lpe.`sales_invoice` IS NOT NULL
		AND (lpe.`invoice` IS NULL OR lpe.`invoice` = '')"""
	)
