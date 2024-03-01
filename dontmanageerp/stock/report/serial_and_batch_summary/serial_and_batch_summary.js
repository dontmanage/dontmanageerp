// Copyright (c) 2023, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Serial and Batch Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": dontmanage.defaults.get_user_default("Company"),
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today()
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
		},
		{
			"fieldname":"voucher_type",
			"label": __("Voucher Type"),
			"fieldtype": "Link",
			"options": "DocType",
			get_query: function() {
				return {
					query: "dontmanageerp.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_voucher_type",
				}
			}
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher No"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				if (!dontmanage.query_report.filters) return;

				let voucher_type = dontmanage.query_report.get_filter_value('voucher_type');
				if (!voucher_type) return;

				return dontmanage.db.get_link_options(voucher_type, txt);
			},
		},
		{
			"fieldname":"serial_no",
			"label": __("Serial No"),
			"fieldtype": "Link",
			"options": "Serial No",
			get_query: function() {
				return {
					query: "dontmanageerp.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_serial_nos",
					filters: {
						"item_code": dontmanage.query_report.get_filter_value('item_code'),
						"voucher_type": dontmanage.query_report.get_filter_value('voucher_type'),
						"voucher_no": dontmanage.query_report.get_filter_value('voucher_no'),
					}
				}
			}
		},
		{
			"fieldname":"batch_no",
			"label": __("Batch No"),
			"fieldtype": "Link",
			"options": "Batch",
			get_query: function() {
				return {
					query: "dontmanageerp.stock.report.serial_and_batch_summary.serial_and_batch_summary.get_batch_nos",
					filters: {
						"item_code": dontmanage.query_report.get_filter_value('item_code'),
						"voucher_type": dontmanage.query_report.get_filter_value('voucher_type'),
						"voucher_no": dontmanage.query_report.get_filter_value('voucher_no'),
					}
				}
			}
		}
	]
};
