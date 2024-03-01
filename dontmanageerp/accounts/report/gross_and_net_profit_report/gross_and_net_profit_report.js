// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Gross and Net Profit Report"] = $.extend(
	{},
	dontmanageerp.financial_statements
);

dontmanage.query_reports["Gross and Net Profit Report"]["filters"].push(
	{
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check"
	}
);
