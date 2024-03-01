// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt



dontmanage.query_reports["COGS By Item Group"] = {
	filters: [
    {
      label: __("Company"),
      fieldname: "company",
      fieldtype: "Link",
      options: "Company",
      mandatory: true,
      default: dontmanage.defaults.get_user_default("Company"),
    },
    {
      label: __("From Date"),
      fieldname: "from_date",
      fieldtype: "Date",
      mandatory: true,
      default: dontmanage.datetime.year_start(),
    },
    {
      label: __("To Date"),
      fieldname: "to_date",
      fieldtype: "Date",
      mandatory: true,
      default: dontmanage.datetime.get_today(),
    },
	]
};
