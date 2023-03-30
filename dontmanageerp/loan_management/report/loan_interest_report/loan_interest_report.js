// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Loan Interest Report"] = {
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
			"fieldname":"applicant_type",
			"label": __("Applicant Type"),
			"fieldtype": "Select",
			"options": ["Customer", "Employee"],
			"reqd": 1,
			"default": "Customer",
			on_change: function() {
				dontmanage.query_report.set_filter_value('applicant', "");
			}
		},
		{
			"fieldname": "applicant",
			"label": __("Applicant"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				var applicant_type = dontmanage.query_report.get_filter_value('applicant_type');
				var applicant = dontmanage.query_report.get_filter_value('applicant');
				if(applicant && !applicant_type) {
					dontmanage.throw(__("Please select Applicant Type first"));
				}
				return applicant_type;
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname":"to_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
	]
};
