// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt



dontmanage.query_reports["Territory-wise Sales"] = {
	"breadcrumb":"Selling",
	"filters": [
		{
			fieldname:"transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [dontmanage.datetime.add_months(dontmanage.datetime.get_today(),-1), dontmanage.datetime.get_today()],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		}
	]
};
