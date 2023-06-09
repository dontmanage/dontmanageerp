// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Quality Procedure', {
	refresh: function(frm) {
		frm.set_query("procedure","processes", (frm) =>{
			return {
				filters: {
					name: ["not in", [frm.parent_quality_procedure, frm.name]]
				}
			};
		});

		frm.set_query('parent_quality_procedure', function(){
			return {
				filters: {
					is_group: 1
				}
			};
		});
	}
});
