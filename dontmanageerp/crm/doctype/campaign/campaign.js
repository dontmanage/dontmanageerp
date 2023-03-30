// Copyright (c) 2021, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Campaign', {
	refresh: function(frm) {
		dontmanageerp.toggle_naming_series();

		if (frm.is_new()) {
			frm.toggle_display("naming_series", dontmanage.boot.sysdefaults.campaign_naming_by=="Naming Series");
		} else {
			cur_frm.add_custom_button(__("View Leads"), function() {
				dontmanage.route_options = {"source": "Campaign", "campaign_name": frm.doc.name};
				dontmanage.set_route("List", "Lead");
			}, "fa fa-list", true);
		}
	}
});
