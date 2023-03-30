// Copyright (c) 2018, DontManage Technologies and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('GoCardless Settings', {
	refresh: function(frm) {
		dontmanageerp.utils.check_payments_app();
	}
});
