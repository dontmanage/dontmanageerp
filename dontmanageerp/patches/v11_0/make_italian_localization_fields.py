# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.regional.italy import state_codes
from dontmanageerp.regional.italy.setup import make_custom_fields, setup_report


def execute():
	company = dontmanage.get_all("Company", filters={"country": "Italy"})
	if not company:
		return

	dontmanage.reload_doc("regional", "report", "electronic_invoice_register")
	make_custom_fields()
	setup_report()

	# Set state codes
	condition = ""
	for state, code in state_codes.items():
		condition += f" when {dontmanage.db.escape(state)} then {dontmanage.db.escape(code)}"

	if condition:
		condition = f"state_code = (case state {condition} end),"

	dontmanage.db.sql(
		f"""
		UPDATE tabAddress set {condition} country_code = UPPER(ifnull((select code
			from `tabCountry` where name = `tabAddress`.country), ''))
			where country_code is null and state_code is null
	"""
	)

	dontmanage.db.sql(
		"""
		UPDATE `tabSales Invoice Item` si, `tabSales Order` so
			set si.customer_po_no = so.po_no, si.customer_po_date = so.po_date
		WHERE
			si.sales_order = so.name and so.po_no is not null
	"""
	)
