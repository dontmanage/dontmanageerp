// Copyright (c) 2016, DontManage Technologies and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Address", {
	is_your_company_address: function(frm) {
		frm.clear_table('links');
		if(frm.doc.is_your_company_address) {
			frm.add_child('links', {
				link_doctype: 'Company',
				link_name: dontmanage.defaults.get_user_default('Company')
			});
			frm.set_query('link_doctype', 'links', () => {
				return {
					filters: {
						name: 'Company'
					}
				};
			});
			frm.refresh_field('links');
		}
		else {
			frm.trigger('refresh');
		}
	}
});
