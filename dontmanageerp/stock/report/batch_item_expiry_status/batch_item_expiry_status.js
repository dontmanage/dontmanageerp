// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.query_reports["Batch Item Expiry Status"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": dontmanage.sys_defaults.year_start_date,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": dontmanage.datetime.get_today()
		}
	]
}
