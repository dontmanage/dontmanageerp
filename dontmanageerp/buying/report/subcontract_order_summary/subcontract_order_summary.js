// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Subcontract Order Summary"] = {
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
			label: __("From Date"),
			fieldname: "from_date",
			fieldtype: "Date",
			default: dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
			reqd: 1
		},
		{
			label: __("To Date"),
			fieldname: "to_date",
			fieldtype: "Date",
			default: dontmanage.datetime.get_today(),
			reqd: 1
		},
		{
			label: __("Order Type"),
			fieldname: "order_type",
			fieldtype: "Select",
			options: ["Purchase Order", "Subcontracting Order"],
			default: "Subcontracting Order"
		},
		{
			label: __("Subcontract Order"),
			fieldname: "name",
			fieldtype: "Data"
		}
	]
};