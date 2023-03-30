// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.require("assets/dontmanageerp/js/sales_trends_filters.js", function() {
	dontmanage.query_reports["Sales Order Trends"] = {
		filters: dontmanageerp.get_sales_trends_filters()
	}
});
