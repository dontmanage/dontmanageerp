dontmanage.listview_settings['Delivery Note'] = {
	add_fields: ["customer", "customer_name", "base_grand_total", "per_installed", "per_billed",
		"transporter_name", "grand_total", "is_return", "status", "currency"],
	get_indicator: function(doc) {
		if(cint(doc.is_return)==1) {
			return [__("Return"), "gray", "is_return,=,Yes"];
		} else if (doc.status === "Closed") {
			return [__("Closed"), "green", "status,=,Closed"];
		} else if (doc.status === "Return Issued") {
			return [__("Return Issued"), "grey", "status,=,Return Issued"];
		} else if (flt(doc.per_billed, 2) < 100) {
			return [__("To Bill"), "orange", "per_billed,<,100"];
		} else if (flt(doc.per_billed, 2) === 100) {
			return [__("Completed"), "green", "per_billed,=,100"];
		}
	},
	onload: function (doclist) {
		const action = () => {
			const selected_docs = doclist.get_checked_items();
			const docnames = doclist.get_checked_items(true);

			if (selected_docs.length > 0) {
				for (let doc of selected_docs) {
					if (!doc.docstatus) {
						dontmanage.throw(__("Cannot create a Delivery Trip from Draft documents."));
					}
				};

				dontmanage.new_doc("Delivery Trip")
					.then(() => {
						// Empty out the child table before inserting new ones
						cur_frm.set_value("delivery_stops", []);

						// We don't want to use `map_current_doc` since it brings up
						// the dialog to select more items. We just want the mapper
						// function to be called.
						dontmanage.call({
							type: "POST",
							method: "dontmanage.model.mapper.map_docs",
							args: {
								"method": "dontmanageerp.stock.doctype.delivery_note.delivery_note.make_delivery_trip",
								"source_names": docnames,
								"target_doc": cur_frm.doc
							},
							callback: function (r) {
								if (!r.exc) {
									dontmanage.model.sync(r.message);
									cur_frm.dirty();
									cur_frm.refresh();
								}
							}
						});
					})
			};
		};

		// doclist.page.add_actions_menu_item(__('Create Delivery Trip'), action, false);

		doclist.page.add_action_item(__('Create Delivery Trip'), action);

		doclist.page.add_action_item(__("Sales Invoice"), ()=>{
			dontmanageerp.bulk_transaction_processing.create(doclist, "Delivery Note", "Sales Invoice");
		});

		doclist.page.add_action_item(__("Packaging Slip From Delivery Note"), ()=>{
			dontmanageerp.bulk_transaction_processing.create(doclist, "Delivery Note", "Packing Slip");
		});
	}
};
