// Copyright (c) 2019, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Quality Feedback', {
	template: function(frm) {
		if (frm.doc.template) {
			frm.call('set_parameters');
		}
	}
});
