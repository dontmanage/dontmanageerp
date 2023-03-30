# Copyright (c) 2020, Wahni Green Technologies and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage

from dontmanageerp.regional.saudi_arabia.setup import add_print_formats


def execute():
	company = dontmanage.get_all("Company", filters={"country": "Saudi Arabia"})
	if company:
		add_print_formats()
		return

	if dontmanage.db.exists("DocType", "Print Format"):
		dontmanage.reload_doc("regional", "print_format", "ksa_vat_invoice", force=True)
		dontmanage.reload_doc("regional", "print_format", "ksa_pos_invoice", force=True)
		for d in ("KSA VAT Invoice", "KSA POS Invoice"):
			dontmanage.db.set_value("Print Format", d, "disabled", 1)
