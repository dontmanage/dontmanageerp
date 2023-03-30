dontmanage.provide('dontmanage.dashboards.chart_sources');

dontmanage.dashboards.chart_sources["Warehouse wise Stock Value"] = {
	method: "dontmanageerp.stock.dashboard_chart_source.warehouse_wise_stock_value.warehouse_wise_stock_value.get",
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: dontmanage.defaults.get_user_default("Company")
		}
	]
};
