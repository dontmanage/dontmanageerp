// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Homepage', {
	refresh: function(frm) {
		frm.add_custom_button(__('Set Meta Tags'), () => {
			dontmanage.utils.set_meta_tag('home');
		});
		frm.add_custom_button(__('Customize Homepage Sections'), () => {
			dontmanage.set_route('List', 'Homepage Section', 'List');
		});
	},
});
