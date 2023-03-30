// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Applicant-Wise Loan Security Exposure"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		}
	]
};
