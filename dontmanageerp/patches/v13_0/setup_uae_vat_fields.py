# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage

from dontmanageerp.regional.united_arab_emirates.setup import setup


def execute():
	company = dontmanage.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	dontmanage.reload_doc("regional", "report", "uae_vat_201")
	dontmanage.reload_doc("regional", "doctype", "uae_vat_settings")
	dontmanage.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
