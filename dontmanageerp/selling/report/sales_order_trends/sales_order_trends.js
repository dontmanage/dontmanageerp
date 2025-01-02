// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.query_reports["Sales Order Trends"] = $.extend({}, dontmanageerp.sales_trends_filters);

dontmanage.query_reports["Sales Order Trends"]["filters"].push({
	fieldname: "include_closed_orders",
	label: __("Include Closed Orders"),
	fieldtype: "Check",
	default: 0,
});
