// Copyright (c) 2024, DontManage and contributors
// For license information, please see license.txt

function get_filters() {
	let filters = [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("Start Date"),
			fieldtype: "Date",
			reqd: 1,
			default: dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
		},
		{
			fieldname: "to_date",
			label: __("End Date"),
			fieldtype: "Date",
			reqd: 1,
			default: dontmanage.datetime.get_today(),
		},
		{
			fieldname: "account",
			label: __("Account"),
			fieldtype: "MultiSelectList",
			options: "Account",
			get_data: function (txt) {
				return dontmanage.db.get_link_options("Account", txt, {
					company: dontmanage.query_report.get_filter_value("company"),
				});
			},
		},
		{
			fieldname: "voucher_no",
			label: __("Voucher No"),
			fieldtype: "Data",
			width: 100,
		},
	];
	return filters;
}

dontmanage.query_reports["Invalid Ledger Entries"] = {
	filters: get_filters(),
};
