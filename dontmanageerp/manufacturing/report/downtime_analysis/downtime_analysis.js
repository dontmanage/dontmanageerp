// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Downtime Analysis"] = {
	"filters": [
		{
			label: __("From Date"),
			fieldname:"from_date",
			fieldtype: "Datetime",
			default: dontmanage.datetime.convert_to_system_tz(dontmanage.datetime.add_months(dontmanage.datetime.now_datetime(), -1)),
			reqd: 1
		},
		{
			label: __("To Date"),
			fieldname:"to_date",
			fieldtype: "Datetime",
			default: dontmanage.datetime.now_datetime(),
			reqd: 1,
		},
		{
			label: __("Machine"),
			fieldname: "workstation",
			fieldtype: "Link",
			options: "Workstation"
		}
	]
};
