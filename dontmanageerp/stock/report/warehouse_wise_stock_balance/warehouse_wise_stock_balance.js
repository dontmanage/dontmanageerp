// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Warehouse Wise Stock Balance"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": dontmanage.defaults.get_user_default("Company")
		}
	],
	"initial_depth": 3,
	"tree": true,
	"parent_field": "parent_warehouse",
	"name_field": "warehouse"
};
