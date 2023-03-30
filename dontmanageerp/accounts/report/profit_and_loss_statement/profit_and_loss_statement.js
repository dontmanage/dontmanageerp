// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt


dontmanage.require("assets/dontmanageerp/js/financial_statements.js", function() {
	dontmanage.query_reports["Profit and Loss Statement"] = $.extend({},
		dontmanageerp.financial_statements);

	dontmanageerp.utils.add_dimensions('Profit and Loss Statement', 10);

	dontmanage.query_reports["Profit and Loss Statement"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
