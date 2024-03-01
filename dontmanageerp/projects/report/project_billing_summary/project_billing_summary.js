// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Project Billing Summary"] = {
	"filters": [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Project",
			reqd: 1
		},
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: dontmanage.datetime.add_months(dontmanage.datetime.month_start(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: dontmanage.datetime.add_days(dontmanage.datetime.month_start(),-1),
			reqd: 1
		},
		{
			fieldname:"include_draft_timesheets",
			label: __("Include Timesheets in Draft Status"),
			fieldtype: "Check",
		},
	]
}
