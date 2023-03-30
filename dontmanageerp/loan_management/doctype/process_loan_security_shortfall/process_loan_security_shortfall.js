// Copyright (c) 2019, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Process Loan Security Shortfall', {
	onload: function(frm) {
		frm.set_value('update_time', dontmanage.datetime.now_datetime());
	}
});
