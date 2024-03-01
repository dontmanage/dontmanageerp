dontmanage.provide("dontmanageerp.bulk_transaction_processing");

$.extend(dontmanageerp.bulk_transaction_processing, {
	create: function(listview, from_doctype, to_doctype) {
		let checked_items = listview.get_checked_items();
		const doc_name = [];
		checked_items.forEach((Item)=> {
			if (Item.docstatus == 0) {
				doc_name.push(Item.name);
			}
		});

		let count_of_rows = checked_items.length;
		dontmanage.confirm(__("Create {0} {1} ?", [count_of_rows, __(to_doctype)]), ()=>{
			if (doc_name.length == 0) {
				dontmanage.call({
					method: "dontmanageerp.utilities.bulk_transaction.transaction_processing",
					args: {data: checked_items, from_doctype: from_doctype, to_doctype: to_doctype}
				}).then(()=> {

				});
				if (count_of_rows > 10) {
					dontmanage.show_alert("Starting a background job to create {0} {1}", [count_of_rows, __(to_doctype)]);
				}
			} else {
				dontmanage.msgprint(__("Selected document must be in submitted state"));
			}
		});
	}
});
