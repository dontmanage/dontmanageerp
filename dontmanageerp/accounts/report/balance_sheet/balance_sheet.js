// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.require("assets/dontmanageerp/js/financial_statements.js", function() {
	dontmanage.query_reports["Balance Sheet"] = $.extend({}, dontmanageerp.financial_statements);

	dontmanageerp.utils.add_dimensions('Balance Sheet', 10);

	dontmanage.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check",
		"default": 1
	});

	dontmanage.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check",
		"default": 1
	});
});
