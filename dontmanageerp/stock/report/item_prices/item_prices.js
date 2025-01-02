// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.query_reports["Item Prices"] = {
	filters: [
		{
			fieldname: "items",
			label: __("Items Filter"),
			fieldtype: "Select",
			options: "Enabled Items only\nDisabled Items only\nAll Items",
			default: "Enabled Items only",
		},
	],
};
