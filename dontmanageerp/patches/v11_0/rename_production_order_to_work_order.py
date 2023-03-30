# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	dontmanage.rename_doc("DocType", "Production Order", "Work Order", force=True)
	dontmanage.reload_doc("manufacturing", "doctype", "work_order")

	dontmanage.rename_doc("DocType", "Production Order Item", "Work Order Item", force=True)
	dontmanage.reload_doc("manufacturing", "doctype", "work_order_item")

	dontmanage.rename_doc("DocType", "Production Order Operation", "Work Order Operation", force=True)
	dontmanage.reload_doc("manufacturing", "doctype", "work_order_operation")

	dontmanage.reload_doc("projects", "doctype", "timesheet")
	dontmanage.reload_doc("stock", "doctype", "stock_entry")
	rename_field("Timesheet", "production_order", "work_order")
	rename_field("Stock Entry", "production_order", "work_order")

	dontmanage.rename_doc(
		"Report", "Production Orders in Progress", "Work Orders in Progress", force=True
	)
	dontmanage.rename_doc("Report", "Completed Production Orders", "Completed Work Orders", force=True)
	dontmanage.rename_doc("Report", "Open Production Orders", "Open Work Orders", force=True)
	dontmanage.rename_doc(
		"Report", "Issued Items Against Production Order", "Issued Items Against Work Order", force=True
	)
	dontmanage.rename_doc(
		"Report", "Production Order Stock Report", "Work Order Stock Report", force=True
	)
