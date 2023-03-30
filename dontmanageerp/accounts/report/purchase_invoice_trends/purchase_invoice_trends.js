// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.require("assets/dontmanageerp/js/purchase_trends_filters.js", function() {
	dontmanage.query_reports["Purchase Invoice Trends"] = {
		filters: dontmanageerp.get_purchase_trends_filters()
	}
});
