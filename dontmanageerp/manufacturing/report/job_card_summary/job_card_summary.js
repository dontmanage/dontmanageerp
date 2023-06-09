// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Job Card Summary"] = {
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
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: dontmanage.defaults.get_user_default("fiscal_year"),
			reqd: 1,
			on_change: function(query_report) {
				var fiscal_year = query_report.get_values().fiscal_year;
				if (!fiscal_year) {
					return;
				}
				dontmanage.model.with_doc("Fiscal Year", fiscal_year, function(r) {
					var fy = dontmanage.model.get_doc("Fiscal Year", fiscal_year);
					dontmanage.query_report.set_filter_value({
						from_date: fy.year_start_date,
						to_date: fy.year_end_date
					});
				});
			}
		},
		{
			label: __("From Posting Date"),
			fieldname:"from_date",
			fieldtype: "Date",
			default: dontmanage.defaults.get_user_default("year_start_date"),
			reqd: 1
		},
		{
			label: __("To Posting Date"),
			fieldname:"to_date",
			fieldtype: "Date",
			default: dontmanage.defaults.get_user_default("year_end_date"),
			reqd: 1,
		},
		{
			label: __("Status"),
			fieldname: "status",
			fieldtype: "Select",
			options: ["", "Open", "Work In Progress", "Completed", "On Hold"]
		},
		{
			label: __("Work Orders"),
			fieldname: "work_order",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return dontmanage.db.get_link_options('Work Order', txt);
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
			label: __("Workstation"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation"
		},
		{
			label: __("Operation"),
			fieldname: "operation",
			fieldtype: "Link",
			options: "Operation"
		}
	]
};
