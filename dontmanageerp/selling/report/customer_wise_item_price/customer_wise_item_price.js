// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Customer-wise Item Price"] = {
	"filters": [
		{
			"label": __("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1
		},
		{
			"label": __("Item"),
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"get_query": () => {
				return {
					query: "dontmanageerp.controllers.queries.item_query",
					filters: { 'is_sales_item': 1 }
				}
			}
		}
	]
}
