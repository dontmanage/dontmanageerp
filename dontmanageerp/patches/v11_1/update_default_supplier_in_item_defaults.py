# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	"""
	default supplier was not set in the item defaults for multi company instance,
	        this patch will set the default supplier

	"""
	if not dontmanage.db.has_column("Item", "default_supplier"):
		return

	dontmanage.reload_doc("stock", "doctype", "item_default")
	dontmanage.reload_doc("stock", "doctype", "item")

	companies = dontmanage.get_all("Company")
	if len(companies) > 1:
		dontmanage.db.sql(
			""" UPDATE `tabItem Default`, `tabItem`
			SET `tabItem Default`.default_supplier = `tabItem`.default_supplier
			WHERE
				`tabItem Default`.parent = `tabItem`.name and `tabItem Default`.default_supplier is null
				and `tabItem`.default_supplier is not null and `tabItem`.default_supplier != '' """
		)
