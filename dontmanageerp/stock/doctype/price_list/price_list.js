// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.ui.form.on("Price List", {
	refresh: function(frm) {
		let me = this;
		frm.add_custom_button(__("Add / Edit Prices"), function() {
			dontmanage.route_options = {
				"price_list": frm.doc.name
			};
			dontmanage.set_route("Report", "Item Price");
		}, "fa fa-money");
	}
});
