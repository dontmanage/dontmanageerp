// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.query_reports["Balance Sheet"] = $.extend(
	{},
	dontmanageerp.financial_statements
);

dontmanageerp.utils.add_dimensions("Balance Sheet", 10);

dontmanage.query_reports["Balance Sheet"]["filters"].push(
	{
		"fieldname": "selected_view",
		"label": __("Select View"),
		"fieldtype": "Select",
		"options": [
			{ "value": "Report", "label": __("Report View") },
			{ "value": "Growth", "label": __("Growth View") }
		],
		"default": "Report",
		"reqd": 1
	},
);

dontmanage.query_reports["Balance Sheet"]["filters"].push({
	fieldname: "accumulated_values",
	label: __("Accumulated Values"),
	fieldtype: "Check",
	default: 1,
});

dontmanage.query_reports["Balance Sheet"]["filters"].push({
	fieldname: "include_default_book_entries",
	label: __("Include Default FB Entries"),
	fieldtype: "Check",
	default: 1,
});