// Copyright (c) 2023, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Packing Slip', {
    setup: (frm) => {
        frm.set_query('delivery_note', () => {
            return {
                filters: {
                    docstatus: 0,
                }
            }
        });

        frm.set_query('item_code', 'items', (doc, cdt, cdn) => {
            if (!doc.delivery_note) {
                dontmanage.throw(__('Please select a Delivery Note'));
            } else {
                let d = locals[cdt][cdn];
                return {
                    query: 'dontmanageerp.stock.doctype.packing_slip.packing_slip.item_details',
                    filters: {
                        delivery_note: doc.delivery_note,
                    }
                }
            }
        });
	},

	refresh: (frm) => {
		frm.toggle_display('misc_details', frm.doc.amended_from);
	},

	delivery_note: (frm) => {
		frm.set_value('items', null);

		if (frm.doc.delivery_note) {
			dontmanageerp.utils.map_current_doc({
				method: 'dontmanageerp.stock.doctype.delivery_note.delivery_note.make_packing_slip',
				source_name: frm.doc.delivery_note,
				target_doc: frm,
				freeze: true,
				freeze_message: __('Creating Packing Slip ...'),
			});
		}
	},
});
