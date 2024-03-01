// Copyright (c) 2017, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Payment Terms Template', {
	refresh: function(frm) {
		frm.fields_dict.terms.grid.toggle_reqd("payment_term", frm.doc.allocate_payment_based_on_payment_terms);
	},

	allocate_payment_based_on_payment_terms: function(frm) {
		frm.fields_dict.terms.grid.toggle_reqd("payment_term", frm.doc.allocate_payment_based_on_payment_terms);
	}
});
