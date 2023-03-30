// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Stock and Account Value Comparison"] = {
	"filters": [
		{
			"label": __("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": dontmanage.defaults.get_user_default("Company")
		},
		{
			"label": __("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			get_query: function() {
				var company = dontmanage.query_report.get_filter_value('company');
				return {
					filters: {
						"account_type": "Stock",
						"company": company
					}
				}
			}
		},
		{
			"label": __("As On Date"),
			"fieldname": "as_on_date",
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today(),
		},
	]
};
