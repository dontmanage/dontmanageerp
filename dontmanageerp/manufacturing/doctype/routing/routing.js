// Copyright (c) 2018, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Routing', {
	refresh: function(frm) {
		frm.trigger("display_sequence_id_column");
	},

	onload: function(frm) {
		frm.trigger("display_sequence_id_column");
	},

	display_sequence_id_column: function(frm) {
		frm.fields_dict.operations.grid.update_docfield_property(
			'sequence_id', 	'in_list_view', 1
		);
	},

	calculate_operating_cost: function(frm, child) {
		const operating_cost = flt(flt(child.hour_rate) * flt(child.time_in_mins) / 60, precision("operating_cost", child));
		dontmanage.model.set_value(child.doctype, child.name, "operating_cost", operating_cost);
	}
});

dontmanage.ui.form.on('BOM Operation', {
	operation: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];

		if(!d.operation) return;

		dontmanage.call({
			"method": "dontmanage.client.get",
			args: {
				doctype: "Operation",
				name: d.operation
			},
			callback: function (data) {
				if (data.message.description) {
					dontmanage.model.set_value(d.doctype, d.name, "description", data.message.description);
				}

				if (data.message.workstation) {
					dontmanage.model.set_value(d.doctype, d.name, "workstation", data.message.workstation);
				}

				frm.events.calculate_operating_cost(frm, d);
			}
		});
	},

	workstation: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];

		dontmanage.call({
			"method": "dontmanage.client.get",
			args: {
				doctype: "Workstation",
				name: d.workstation
			},
			callback: function (data) {
				dontmanage.model.set_value(d.doctype, d.name, "hour_rate", data.message.hour_rate);
				frm.events.calculate_operating_cost(frm, d);
			}
		});
	},

	time_in_mins: function(frm, cdt, cdn) {
		const d = locals[cdt][cdn];
		frm.events.calculate_operating_cost(frm, d);
	}
});

dontmanage.tour['Routing'] = [
	{
		fieldname: "routing_name",
		title: "Routing Name",
		description: __("Enter a name for Routing.")
	},
	{
		fieldname: "operations",
		title: "BOM Operations",
		description: __("Enter the Operation, the table will fetch the Operation details like Hourly Rate, Workstation automatically.\n\n After that, set the Operation Time in minutes and the table will calculate the Operation Costs based on the Hourly Rate and Operation Time.")
	}
];
