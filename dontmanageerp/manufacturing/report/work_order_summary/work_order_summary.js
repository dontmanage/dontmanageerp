// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Work Order Summary"] = {
	"filters": [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			label: __("Based On"),
			fieldname:"based_on",
			fieldtype: "Select",
			options: "Creation Date\nPlanned Date\nActual Date",
			default: "Creation Date"
		},
		{
			label: __("From Posting Date"),
			fieldname:"from_date",
			fieldtype: "Date",
			default: dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -3),
			reqd: 1
		},
		{
			label: __("To Posting Date"),
			fieldname:"to_date",
			fieldtype: "Date",
			default: dontmanage.datetime.get_today(),
			reqd: 1,
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "Not Started", "In Process", "Completed", "Stopped", "Closed"]
		},
		{
			label: __("Sales Orders"),
			fieldname: "sales_order",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Sales Order', txt);
			}
		},
		{
			label: __("Production Item"),
			fieldname: "production_item",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Item', txt);
			}
		},
		{
			label: __("Age"),
			fieldname:"age",
			fieldtype: "Int",
			default: "0"
		},
		{
			label: __("Charts Based On"),
			fieldname:"charts_based_on",
			fieldtype: "Select",
			options: ["Status", "Age", "Quantity"],
			default: "Status"
		},
	]
};
