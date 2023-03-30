// Copyright (c) 2017, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Manufacturer', {
	refresh: function(frm) {
		dontmanage.dynamic_link = { doc: frm.doc, fieldname: 'name', doctype: 'Manufacturer' };
		if (frm.doc.__islocal) {
			hide_field(['address_html','contact_html']);
			dontmanage.contacts.clear_address_and_contact(frm);
		}
		else {
			unhide_field(['address_html','contact_html']);
			dontmanage.contacts.render_address_and_contact(frm);
		}
	}
});
