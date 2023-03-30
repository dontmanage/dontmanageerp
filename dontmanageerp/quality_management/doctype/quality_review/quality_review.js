// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Quality Review', {
	goal: function(frm) {
		dontmanage.call({
			"method": "dontmanage.client.get",
			args: {
				doctype: "Quality Goal",
				name: frm.doc.goal
			},
			callback: function(data){
				frm.fields_dict.reviews.grid.remove_all();
				let objectives = data.message.objectives;
				for (var i in objectives) {
					frm.add_child("reviews");
					frm.fields_dict.reviews.get_value()[i].objective = objectives[i].objective;
					frm.fields_dict.reviews.get_value()[i].target = objectives[i].target;
					frm.fields_dict.reviews.get_value()[i].uom = objectives[i].uom;
				}
				frm.refresh();
			}
		});
	},
});
