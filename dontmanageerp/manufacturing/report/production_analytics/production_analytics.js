// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Production Analytics"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today(), true)[1],
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today(), true)[2],
			reqd: 1
		},
		{
			fieldname: "range",
			label: __("Range"),
			fieldtype: "Select",
			options: [
				{ "value": "Weekly", "label": __("Weekly") },
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Yearly", "label": __("Yearly") }
			],
			default: "Monthly",
			reqd: 1
		}
	]
}
