// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.query_reports["Batch Item Expiry Status"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": dontmanageerp.utils.get_fiscal_year(dontmanage.datetime.get_today(), true)[1],
			"reqd": 1,
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": dontmanage.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname":"item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "100",
			"get_query": function () {
				return {
					filters: {"has_batch_no": 1}
				}
			}
		}
	]
}
