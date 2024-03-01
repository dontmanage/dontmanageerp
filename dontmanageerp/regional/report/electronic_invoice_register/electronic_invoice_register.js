// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Electronic Invoice Register"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today()
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company")
		},
	],
	"onload": function(reportview) {
		reportview.page.add_inner_button(__("Export E-Invoices"), function() {
			//TODO: refactor condition to disallow export if report has no data.
			if (!reportview.data.length) {
				dontmanage.msgprint(__("No data to export"));
				return
			}

			var w = window.open(
				dontmanage.urllib.get_full_url(
					"/api/method/dontmanageerp.regional.italy.utils.export_invoices?"
					+ "filters=" + JSON.stringify(reportview.get_filter_values())
				)
			);
			if (!w) {
				dontmanage.msgprint(__("Please enable pop-ups")); return;
			}
		})
	}
}
