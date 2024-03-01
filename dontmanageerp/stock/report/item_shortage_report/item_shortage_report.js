// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Item Shortage Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"reqd": 1,
			"default": dontmanage.defaults.get_default("company")
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "MultiSelectList",
			"width": "100",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Warehouse', txt);
			}
		}
	]
};
