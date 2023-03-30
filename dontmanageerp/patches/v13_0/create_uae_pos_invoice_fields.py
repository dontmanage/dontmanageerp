# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = dontmanage.get_all(
		"Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]}
	)
	if not company:
		return

	dontmanage.reload_doc("accounts", "doctype", "pos_invoice")
	dontmanage.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()
