// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Project Update', {
	refresh: function() {

	},

	onload: function (frm) {
		frm.set_value("naming_series", "UPDATE-.project.-.YY.MM.DD.-.####");
	},

	validate: function (frm) {
		frm.set_value("time", dontmanage.datetime.now_time());
		frm.set_value("date", dontmanage.datetime.nowdate());
	}
});
