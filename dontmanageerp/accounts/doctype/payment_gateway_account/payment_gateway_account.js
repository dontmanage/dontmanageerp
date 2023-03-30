// Copyright (c) 2019, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.ui.form.on('Payment Gateway Account', {
	refresh(frm) {
		dontmanageerp.utils.check_payments_app();
		if(!frm.doc.__islocal) {
			frm.set_df_property('payment_gateway', 'read_only', 1);
		}
	}
});
