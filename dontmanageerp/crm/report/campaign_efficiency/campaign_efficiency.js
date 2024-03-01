// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
dontmanage.query_reports["Campaign Efficiency"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today(), true)[1],
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today(), true)[2],
		}
	]
};
