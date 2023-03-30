// Copyright (c) 2013, DontManage and contributors
// For license information, please see license.txt

dontmanage.require("assets/dontmanageerp/js/financial_statements.js", function() {
	dontmanage.query_reports["Cash Flow"] = $.extend({},
		dontmanageerp.financial_statements);

	dontmanageerp.utils.add_dimensions('Cash Flow', 10);

	// The last item in the array is the definition for Presentation Currency
	// filter. It won't be used in cash flow for now so we pop it. Please take
	// of this if you are working here.

	dontmanage.query_reports["Cash Flow"]["filters"].splice(8, 1);

	dontmanage.query_reports["Cash Flow"]["filters"].push(
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
