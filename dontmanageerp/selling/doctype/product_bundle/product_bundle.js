// Copyright (c) 2021, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.ui.form.on("Product Bundle", {
	refresh: function (frm) {
		frm.toggle_enable("new_item_code", frm.is_new());
		frm.set_query("new_item_code", () => {
			return {
				query: "dontmanageerp.selling.doctype.product_bundle.product_bundle.get_new_item_code",
			};
		});
	},
});
