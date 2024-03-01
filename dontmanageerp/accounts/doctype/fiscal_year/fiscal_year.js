// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.ui.form.on('Fiscal Year', {
	onload: function(frm) {
		if(frm.doc.__islocal) {
			frm.set_value("year_start_date",
				dontmanage.datetime.add_days(dontmanage.defaults.get_default("year_end_date"), 1));
		}
	},
	year_start_date: function(frm) {
		if (!frm.doc.is_short_year) {
			let year_end_date =
				dontmanage.datetime.add_days(dontmanage.datetime.add_months(frm.doc.year_start_date, 12), -1);
			frm.set_value("year_end_date", year_end_date);
		}
	},
});
