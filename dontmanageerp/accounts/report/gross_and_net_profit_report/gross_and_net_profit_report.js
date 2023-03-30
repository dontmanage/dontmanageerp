// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Gross and Net Profit Report"] = {
	"filters": [

	]
}
dontmanage.require("assets/dontmanageerp/js/financial_statements.js", function() {
	dontmanage.query_reports["Gross and Net Profit Report"] = $.extend({},
		dontmanageerp.financial_statements);

	dontmanage.query_reports["Gross and Net Profit Report"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "accumulated_values",
			"label": __("Accumulated Values"),
			"fieldtype": "Check"
		}
	);
});
