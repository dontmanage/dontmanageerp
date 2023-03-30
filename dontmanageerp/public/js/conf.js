// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.provide('dontmanageerp');

// preferred modules for breadcrumbs
$.extend(dontmanage.breadcrumbs.preferred, {
	"Item Group": "Stock",
	"Customer Group": "Selling",
	"Supplier Group": "Buying",
	"Territory": "Selling",
	"Sales Person": "Selling",
	"Sales Partner": "Selling",
	"Brand": "Stock",
	"Maintenance Schedule": "Support",
	"Maintenance Visit": "Support"
});

$.extend(dontmanage.breadcrumbs.module_map, {
	'DontManageErp Integrations': 'Integrations',
	'Geo': 'Settings',
	'Portal': 'Website',
	'Utilities': 'Settings',
	'E-commerce': 'Website',
	'Contacts': 'CRM'
});
