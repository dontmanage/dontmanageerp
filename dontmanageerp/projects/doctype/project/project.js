// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt
dontmanage.ui.form.on("Project", {
	setup(frm) {
		frm.make_methods = {
			'Timesheet': () => {
				open_form(frm, "Timesheet", "Timesheet Detail", "time_logs");
			},
			'Purchase Order': () => {
				open_form(frm, "Purchase Order", "Purchase Order Item", "items");
			},
			'Purchase Receipt': () => {
				open_form(frm, "Purchase Receipt", "Purchase Receipt Item", "items");
			},
			'Purchase Invoice': () => {
				open_form(frm, "Purchase Invoice", "Purchase Invoice Item", "items");
			},
		};
	},
	onload: function (frm) {
		const so = frm.get_docfield("sales_order");
		so.get_route_options_for_new_doc = () => {
			if (frm.is_new()) return {};
			return {
				"customer": frm.doc.customer,
				"project_name": frm.doc.name
			};
		};

		frm.set_query('customer', 'dontmanageerp.controllers.queries.customer_query');

		frm.set_query("user", "users", function () {
			return {
				query: "dontmanageerp.projects.doctype.project.project.get_users_for_project"
			};
		});

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'project': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/projects?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
		frm.trigger("set_custom_buttons");
	},

	set_custom_buttons: function(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__('Duplicate Project with Tasks'), () => {
				frm.events.create_duplicate(frm);
			}, __("Actions"));

			frm.add_custom_button(__('Update Total Purchase Cost'), () => {
				frm.events.update_total_purchase_cost(frm);
			}, __("Actions"));

			frm.trigger("set_project_status_button");


			if (dontmanage.model.can_read("Task")) {
				frm.add_custom_button(__("Gantt Chart"), function () {
					dontmanage.route_options = {
						"project": frm.doc.name
					};
					dontmanage.set_route("List", "Task", "Gantt");
				}, __("View"));

				frm.add_custom_button(__("Kanban Board"), () => {
					dontmanage.call('dontmanageerp.projects.doctype.project.project.create_kanban_board_if_not_exists', {
						project: frm.doc.name
					}).then(() => {
						dontmanage.set_route('List', 'Task', 'Kanban', frm.doc.project_name);
					});
				}, __("View"));
			}
		}


	},

	update_total_purchase_cost: function(frm) {
		dontmanage.call({
			method: "dontmanageerp.projects.doctype.project.project.recalculate_project_total_purchase_cost",
			args: {project: frm.doc.name},
			freeze: true,
			freeze_message: __('Recalculating Purchase Cost against this Project...'),
			callback: function(r) {
				if (r && !r.exc) {
					dontmanage.msgprint(__('Total Purchase Cost has been updated'));
					frm.refresh();
				}
			}

		});
	},

	set_project_status_button: function(frm) {
		frm.add_custom_button(__('Set Project Status'), () => {
			let d = new dontmanage.ui.Dialog({
				"title": __("Set Project Status"),
				"fields": [
					{
						"fieldname": "status",
						"fieldtype": "Select",
						"label": "Status",
						"reqd": 1,
						"options": "Completed\nCancelled",
					},
				],
				primary_action: function() {
					frm.events.set_status(frm, d.get_values().status);
					d.hide();
				},
				primary_action_label: __("Set Project Status")
			}).show();
		}, __("Actions"));
	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
			dontmanage.prompt('Project Name', (data) => {
				dontmanage.xcall('dontmanageerp.projects.doctype.project.project.create_duplicate_project',
					{
						prev_doc: frm.doc,
						project_name: data.value
					}).then(() => {
					dontmanage.set_route('Form', "Project", data.value);
					dontmanage.show_alert(__("Duplicate project has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
		dontmanage.confirm(__('Set Project and all Tasks to status {0}?', [status.bold()]), () => {
			dontmanage.xcall('dontmanageerp.projects.doctype.project.project.set_project_status',
				{project: frm.doc.name, status: status}).then(() => {
				frm.reload_doc();
			});
		});
	},

});

function open_form(frm, doctype, child_doctype, parentfield) {
	dontmanage.model.with_doctype(doctype, () => {
		let new_doc = dontmanage.model.get_new_doc(doctype);

		// add a new row and set the project
		let new_child_doc = dontmanage.model.get_new_doc(child_doctype);
		new_child_doc.project = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = doctype;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		dontmanage.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});

}
