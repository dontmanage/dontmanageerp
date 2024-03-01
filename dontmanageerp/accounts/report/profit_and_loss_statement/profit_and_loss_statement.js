// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.query_reports["Profit and Loss Statement"] = $.extend(
	{},
	dontmanageerp.financial_statements
);

dontmanageerp.utils.add_dimensions("Profit and Loss Statement", 10);

dontmanage.query_reports["Profit and Loss Statement"]["filters"].push(
	{
		"fieldname": "selected_view",
		"label": __("Select View"),
		"fieldtype": "Select",
		"options": [
			{ "value": "Report", "label": __("Report View") },
			{ "value": "Growth", "label": __("Growth View") },
			{ "value": "Margin", "label": __("Margin View") },
		],
		"default": "Report",
		"reqd": 1
	},
);

dontmanage.query_reports["Profit and Loss Statement"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
	default: 1,
});
