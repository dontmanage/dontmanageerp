// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


function get_filters() {
	let filters = [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"filter_based_on",
			"label": __("Filter Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year", "Date Range"],
			"default": ["Fiscal Year"],
			"reqd": 1,
			on_change: function() {
				let filter_based_on = dontmanage.query_report.get_filter_value('filter_based_on');
				dontmanage.query_report.toggle_filter_display('from_fiscal_year', filter_based_on === 'Date Range');
				dontmanage.query_report.toggle_filter_display('to_fiscal_year', filter_based_on === 'Date Range');
				dontmanage.query_report.toggle_filter_display('period_start_date', filter_based_on === 'Fiscal Year');
				dontmanage.query_report.toggle_filter_display('period_end_date', filter_based_on === 'Fiscal Year');

				dontmanage.query_report.refresh();
			}
		},
		{
			"fieldname":"period_start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"hidden": 1,
			"reqd": 1
		},
		{
			"fieldname":"period_end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"hidden": 1,
			"reqd": 1
		},
		{
			"fieldname":"from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today()),
			"reqd": 1
		},
		{
			"fieldname":"to_fiscal_year",
			"label": __("End Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today()),
			"reqd": 1
		},
		{
			"fieldname": "periodicity",
			"label": __("Periodicity"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Half-Yearly", "label": __("Half-Yearly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			"default": "Monthly",
			"reqd": 1
		},
		{
			"fieldname": "type",
			"label": __("Invoice Type"),
			"fieldtype": "Select",
			"options": [
				{ "value": "Revenue", "label": __("Revenue") },
				{ "value": "Expense", "label": __("Expense") }
			],
			"default": "Revenue",
			"reqd": 1
		},
		{
			"fieldname" : "with_upcoming_postings",
			"label": __("Show with upcoming revenue/expense"),
			"fieldtype": "Check",
			"default": 1
		}
	]

	return filters;
}

dontmanage.query_reports["Deferred Revenue and Expense"] = {
	"filters": get_filters(),
	"formatter": function(value, row, column, data, default_formatter){
		return default_formatter(value, row, column, data);
	},
	onload: function(report){
		let fiscal_year = dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today());

		dontmanage.model.with_doc("Fiscal Year", fiscal_year, function(r) {
			var fy = dontmanage.model.get_doc("Fiscal Year", fiscal_year);
			dontmanage.query_report.set_filter_value({
				period_start_date: fy.year_start_date,
				period_end_date: fy.year_end_date
			});
		});
	}
};

