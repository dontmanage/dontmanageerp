dontmanageerp.setup_e_invoice_button = (doctype) => {
	dontmanage.ui.form.on(doctype, {
		refresh: (frm) => {
			if(frm.doc.docstatus == 1) {
				frm.add_custom_button('Generate E-Invoice', () => {
					frm.call({
						method: "dontmanageerp.regional.italy.utils.generate_single_invoice",
						args: {
							docname: frm.doc.name
						},
						callback: function(r) {
							frm.reload_doc();
							if(r.message) {
								open_url_post(dontmanage.request.url, {
									cmd: 'dontmanage.core.doctype.file.file.download_file',
									file_url: r.message
								});
							}
						}
					});
				});
			}
		}
	});
};
