// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.query_reports["Daily Timesheet Summary"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today()
		},
	]
}
