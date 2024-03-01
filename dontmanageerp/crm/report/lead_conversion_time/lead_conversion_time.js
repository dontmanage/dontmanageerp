// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Lead Conversion Time"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default": dontmanage.datetime.add_days(dontmanage.datetime.nowdate(), -30)
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			'reqd': 1,
			"default":dontmanage.datetime.nowdate()
		},
	]
};
