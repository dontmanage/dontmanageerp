// Copyright (c) 2020, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('UAE VAT Settings', {
	onload: function(frm) {
		frm.set_query('account', 'uae_vat_accounts', function() {
			return {
				filters: {
					'company': frm.doc.company
				}
			};
		});
	}
});
