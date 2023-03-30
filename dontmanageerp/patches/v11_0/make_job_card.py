# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	dontmanage.reload_doc("manufacturing", "doctype", "work_order")
	dontmanage.reload_doc("manufacturing", "doctype", "work_order_item")
	dontmanage.reload_doc("manufacturing", "doctype", "job_card")
	dontmanage.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = dontmanage.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = dontmanage.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in dontmanage.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = dontmanage.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			dontmanage.delete_doc("Timesheet", d.name)
