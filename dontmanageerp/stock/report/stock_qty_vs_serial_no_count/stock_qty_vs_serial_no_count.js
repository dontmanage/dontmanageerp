// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Stock Qty vs Serial No Count"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"get_query": function() {
				const company = dontmanage.query_report.get_filter_value('company');
				return {
					filters: { 'company': company }
				}
			},
			"reqd": 1
		},
	],

	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "difference" && data) {
			if (data.difference > 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
			else if (data.difference < 0) {
				value = "<span style='color:red'>" + value + "</span>";
			}
		}
		return value;
	}
};
