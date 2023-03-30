// Copyright (c) 2017, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Driver", {
	setup: function(frm) {
		frm.set_query("transporter", function() {
			return {
				filters: {
					is_transporter: 1
				}
			};
		});
	},

	refresh: function(frm) {
		frm.set_query("address", function() {
			return {
				filters: {
					is_your_company_address: !frm.doc.transporter ? 1 : 0
				}
			};
		});
	},

	transporter: function(frm, cdt, cdn) {
		// this assumes that supplier's address has same title as supplier's name
		dontmanage.db
			.get_doc("Address", null, { address_title: frm.doc.transporter })
			.then(r => {
				dontmanage.model.set_value(cdt, cdn, "address", r.name);
			})
			.catch(err => {
				console.log(err);
			});
	}
});
