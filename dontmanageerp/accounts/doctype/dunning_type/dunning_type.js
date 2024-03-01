// Copyright (c) 2020, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on("Dunning Type", {
	setup: function (frm) {
		frm.set_query("income_account", () => {
			return {
				filters: {
					root_type: "Income",
					is_group: 0,
					company: frm.doc.company,
				},
			};
		});
		frm.set_query("cost_center", () => {
			return {
				filters: {
					is_group: 0,
					company: frm.doc.company,
				},
			};
		});
	},
});