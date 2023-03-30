// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports["Serial No Ledger"] = {
	"filters": [
		{
			'label': __('Item Code'),
			'fieldtype': 'Link',
			'fieldname': 'item_code',
			'reqd': 1,
			'options': 'Item',
			get_query: function() {
				return {
					filters: {
						'has_serial_no': 1
					}
				}
			}
		},
		{
			'label': __('Serial No'),
			'fieldtype': 'Link',
			'fieldname': 'serial_no',
			'options': 'Serial No',
			'reqd': 1
		},
		{
			'label': __('Warehouse'),
			'fieldtype': 'Link',
			'fieldname': 'warehouse',
			'options': 'Warehouse',
			get_query: function() {
				let company = dontmanage.query_report.get_filter_value('company');

				if (company) {
					return {
						filters: {
							'company': company
						}
					}
				}
			}
		},
		{
			'label': __('As On Date'),
			'fieldtype': 'Date',
			'fieldname': 'posting_date',
			'default': dontmanage.datetime.get_today()
		},
	]
};
