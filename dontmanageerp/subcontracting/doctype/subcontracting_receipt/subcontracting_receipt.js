// Copyright (c) 2022, DontManage and contributors
// For license information, please see license.txt

dontmanage.provide('dontmanageerp.buying');

{% include 'dontmanageerp/stock/landed_taxes_and_charges_common.js' %};

dontmanage.ui.form.on('Subcontracting Receipt', {
	setup: (frm) => {
		frm.get_field('supplied_items').grid.cannot_add_rows = true;
		frm.get_field('supplied_items').grid.only_sortable();

		frm.set_query('set_warehouse', () => {
			return {
				filters: {
					company: frm.doc.company,
					is_group: 0
				}
			};
		});

		frm.set_query('rejected_warehouse', () => {
			return {
				filters: {
					company: frm.doc.company,
					is_group: 0
				}
			};
		});

		frm.set_query('supplier_warehouse', () => {
			return {
				filters: {
					company: frm.doc.company,
					is_group: 0
				}
			};
		});

		frm.set_query('warehouse', 'items', () => ({
			filters: {
				company: frm.doc.company,
				is_group: 0
			}
		}));

		frm.set_query('rejected_warehouse', 'items', () => ({
			filters: {
				company: frm.doc.company,
				is_group: 0
			}
		}));

		frm.set_query('expense_account', 'items', function () {
			return {
				query: 'dontmanageerp.controllers.queries.get_expense_account',
				filters: { 'company': frm.doc.company }
			};
		});

		frm.set_query('batch_no', 'items', function(doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			return {
				filters: {
					item: row.item_code
				}
			}
		});

		let batch_no_field = frm.get_docfield("items", "batch_no");
		if (batch_no_field) {
			batch_no_field.get_route_options_for_new_doc = function(row) {
				return {
					"item": row.doc.item_code
				}
			};
		}

		dontmanage.db.get_single_value('Buying Settings', 'backflush_raw_materials_of_subcontract_based_on').then(val => {
			if (val == 'Material Transferred for Subcontract') {
				frm.fields_dict['supplied_items'].grid.grid_rows.forEach((grid_row) => {
					grid_row.docfields.forEach((df) => {
						if (df.fieldname == 'consumed_qty') {
							df.read_only = 0;
						}
					});
				});
			}
		});
	},

	refresh: (frm) => {
		if (frm.doc.docstatus > 0) {
			frm.add_custom_button(__('Stock Ledger'), function () {
				dontmanage.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				dontmanage.set_route('query-report', 'Stock Ledger');
			}, __('View'));

			frm.add_custom_button(__('Accounting Ledger'), function () {
				dontmanage.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: 'Group by Voucher (Consolidated)',
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				dontmanage.set_route('query-report', 'General Ledger');
			}, __('View'));
		}

		if (!frm.doc.is_return && frm.doc.docstatus == 1 && frm.doc.per_returned < 100) {
			frm.add_custom_button(__('Subcontract Return'), function () {
				dontmanage.model.open_mapped_doc({
					method: 'dontmanageerp.subcontracting.doctype.subcontracting_receipt.subcontracting_receipt.make_subcontract_return',
					frm: frm
				});
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}

		if (frm.doc.docstatus == 0) {
			frm.add_custom_button(__('Subcontracting Order'), function () {
				if (!frm.doc.supplier) {
					dontmanage.throw({
						title: __('Mandatory'),
						message: __('Please Select a Supplier')
					});
				}

				dontmanageerp.utils.map_current_doc({
					method: 'dontmanageerp.subcontracting.doctype.subcontracting_order.subcontracting_order.make_subcontracting_receipt',
					source_doctype: 'Subcontracting Order',
					target: frm,
					setters: {
						supplier: frm.doc.supplier,
					},
					get_query_filters: {
						docstatus: 1,
						per_received: ['<', 100],
						company: frm.doc.company
					}
				});
			}, __('Get Items From'));
		}
	},

	set_warehouse: (frm) => {
		set_warehouse_in_children(frm.doc.items, 'warehouse', frm.doc.set_warehouse);
	},

	rejected_warehouse: (frm) => {
		set_warehouse_in_children(frm.doc.items, 'rejected_warehouse', frm.doc.rejected_warehouse);
	},
});

dontmanage.ui.form.on('Landed Cost Taxes and Charges', {
	amount: function (frm, cdt, cdn) {
		frm.events.set_base_amount(frm, cdt, cdn);
	},

	expense_account: function (frm, cdt, cdn) {
		frm.events.set_account_currency(frm, cdt, cdn);
	}
});

dontmanage.ui.form.on('Subcontracting Receipt Item', {
	item_code(frm) {
		set_missing_values(frm);
	},

	qty(frm) {
		set_missing_values(frm);
	},

	rate(frm) {
		set_missing_values(frm);
	},
});

dontmanage.ui.form.on('Subcontracting Receipt Supplied Item', {
	consumed_qty(frm) {
		set_missing_values(frm);
	},
});

let set_warehouse_in_children = (child_table, warehouse_field, warehouse) => {
	let transaction_controller = new dontmanageerp.TransactionController();
	transaction_controller.autofill_warehouse(child_table, warehouse_field, warehouse);
};

let set_missing_values = (frm) => {
	dontmanage.call({
		doc: frm.doc,
		method: 'set_missing_values',
		callback: (r) => {
			if (!r.exc) frm.refresh();
		},
	});
};