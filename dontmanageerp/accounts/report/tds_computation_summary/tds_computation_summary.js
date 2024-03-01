// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["TDS Computation Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_default('company')
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Select",
			"options": ["Supplier", "Customer"],
			"reqd": 1,
			"default": "Supplier",
			"on_change": function(){
				dontmanage.query_report.set_filter_value("party", "");
			}
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				var party_type = dontmanage.query_report.get_filter_value('party_type');
				var party = dontmanage.query_report.get_filter_value('party');
				if(party && !party_type) {
					dontmanage.throw(__("Please select Party Type first"));
				}
				return party_type;
			},
			"get_query": function() {
				return {
					"filters": {
						"tax_withholding_category": ["!=",""],
					}
				}
			},
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		}
	]
}
