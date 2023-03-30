# Copyright (c) 2020, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage

from dontmanageerp.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = dontmanage.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	dontmanage.reload_doc("regional", "doctype", "south_africa_vat_settings")
	dontmanage.reload_doc("regional", "report", "vat_audit_report")
	dontmanage.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
