// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Requested Items to Order and Receive"] = {
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
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": dontmanage.datetime.get_today()
		},
		{
			"fieldname": "material_request",
			"label": __("Material Request"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Material Request",
			"get_query": () => {
				return {
					filters: {
						"docstatus": 1,
						"material_request_type": "Purchase",
						"per_received": ["<", 100]
					}
				}
			}
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item",
			"get_query": () => {
				return {
					query: "dontmanageerp.controllers.queries.item_query"
				}
			}
		},
		{
			"fieldname": "group_by_mr",
			"label": __("Group by Material Request"),
			"fieldtype": "Check",
			"default": 0
		}
	],

	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname == "ordered_qty" && data && data.ordered_qty > 0) {
			value = "<span style='color:green'>" + value + "</span>";
		}
		return value;
	}
};
