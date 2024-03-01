// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Lost Opportunity"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -12),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"lost_reason",
			"label": __("Lost Reason"),
			"fieldtype": "Link",
			"options": "Opportunity Lost Reason"
		},
		{
			"fieldname":"territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory"
		},
		{
			"fieldname":"opportunity_from",
			"label": __("Opportunity From"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function() {
				return {
					"filters": {
						"name": ["in", ["Customer", "Lead"]],
					}
				}
			}
		},
		{
			"fieldname":"party_name",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"options": "opportunity_from"
		},
	]
};
