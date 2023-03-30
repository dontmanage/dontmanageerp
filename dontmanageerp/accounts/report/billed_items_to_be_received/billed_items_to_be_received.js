// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

dontmanage.query_reports['Billed Items To Be Received'] = {
	'filters': [
		{
			'label': __('Company'),
			'fieldname': 'company',
			'fieldtype': 'Link',
			'options': 'Company',
			'reqd': 1,
			'default': dontmanage.defaults.get_default('Company')
		},
		{
			'label': __('As on Date'),
			'fieldname': 'posting_date',
			'fieldtype': 'Date',
			'reqd': 1,
			'default': get_today()
		},
		{
			'label': __('Purchase Invoice'),
			'fieldname': 'purchase_invoice',
			'fieldtype': 'Link',
			'options': 'Purchase Invoice'
		}
	]
};
