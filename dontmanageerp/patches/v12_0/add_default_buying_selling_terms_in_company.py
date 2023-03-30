# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	dontmanage.reload_doc("setup", "doctype", "company")
	if dontmanage.db.has_column("Company", "default_terms"):
		rename_field("Company", "default_terms", "default_selling_terms")

		for company in dontmanage.get_all(
			"Company", ["name", "default_selling_terms", "default_buying_terms"]
		):
			if company.default_selling_terms and not company.default_buying_terms:
				dontmanage.db.set_value(
					"Company", company.name, "default_buying_terms", company.default_selling_terms
				)

	dontmanage.reload_doc("setup", "doctype", "terms_and_conditions")
	dontmanage.db.sql("update `tabTerms and Conditions` set selling=1, buying=1, hr=1")
