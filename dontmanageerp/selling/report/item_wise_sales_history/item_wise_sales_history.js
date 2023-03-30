// Copyright (c) 2019, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Item-wise Sales History"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname:"from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			reqd: 1,
			default: dontmanage.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
		{
			fieldname:"item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group"
		},
		{
			fieldname:"item_code",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			get_query: () => {
				return {
					query: "dontmanageerp.controllers.queries.item_query"
				}
			}
		},
		{
			fieldname:"customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer"
		}
	],

	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		let format_fields = ["delivered_quantity", "billed_amount"];

		if (in_list(format_fields, column.fieldname) && data && data[column.fieldname] > 0) {
			value = "<span style='color:green;'>" + value + "</span>";
		}
		return value;
	}
};
