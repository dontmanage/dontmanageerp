// Copyright (c) 2020, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('Process Statement Of Accounts', {
	view_properties: function(frm) {
		dontmanage.route_options = {doc_type: 'Customer'};
		dontmanage.set_route("Form", "Customize Form");
	},
	refresh: function(frm){
		if(!frm.doc.__islocal) {
			frm.add_custom_button(__('Send Emails'), function(){
				dontmanage.call({
					method: "dontmanageerp.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.send_emails",
					args: {
						"document_name": frm.doc.name,
					},
					callback: function(r) {
						if(r && r.message) {
							dontmanage.show_alert({message: __('Emails Queued'), indicator: 'blue'});
						}
						else{
							dontmanage.msgprint(__('No Records for these settings.'))
						}
					}
				});
			});
			frm.add_custom_button(__('Download'), function(){
				var url = dontmanage.urllib.get_full_url(
					'/api/method/dontmanageerp.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.download_statements?'
					+ 'document_name='+encodeURIComponent(frm.doc.name))
				$.ajax({
					url: url,
					type: 'GET',
					success: function(result) {
						if(jQuery.isEmptyObject(result)){
							dontmanage.msgprint(__('No Records for these settings.'));
						}
						else{
							window.location = url;
						}
					}
				});
			});
		}
	},
	onload: function(frm) {
		frm.set_query('currency', function(){
			return {
				filters: {
					'enabled': 1
				}
			}
		});
		frm.set_query("account", function() {
			return {
				filters: {
					'company': frm.doc.company
				}
			};
		});
		if(frm.doc.__islocal){
			frm.set_value('from_date', dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1));
			frm.set_value('to_date', dontmanage.datetime.get_today());
		}
	},
	customer_collection: function(frm){
		frm.set_value('collection_name', '');
		if(frm.doc.customer_collection){
			frm.get_field('collection_name').set_label(frm.doc.customer_collection);
		}
	},
	frequency: function(frm){
		if(frm.doc.frequency != ''){
			frm.set_value('start_date', dontmanage.datetime.get_today());
		}
		else{
			frm.set_value('start_date', '');
		}
	},
	fetch_customers: function(frm){
		if(frm.doc.collection_name){
			dontmanage.call({
				method: "dontmanageerp.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.fetch_customers",
				args: {
					'customer_collection': frm.doc.customer_collection,
					'collection_name': frm.doc.collection_name,
					'primary_mandatory': frm.doc.primary_mandatory
				},
				callback: function(r) {
					if(!r.exc) {
						if(r.message.length){
							frm.clear_table('customers');
							for (const customer of r.message){
								var row = frm.add_child('customers');
								row.customer = customer.name;
								row.primary_email = customer.primary_email;
								row.billing_email = customer.billing_email;
							}
							frm.refresh_field('customers');
						}
						else{
							dontmanage.throw(__('No Customers found with selected options.'));
						}
					}
				}
			});
		}
		else {
			dontmanage.throw('Enter ' + frm.doc.customer_collection + ' name.');
		}
	}
});

dontmanage.ui.form.on('Process Statement Of Accounts Customer', {
	customer: function(frm, cdt, cdn){
		var row = locals[cdt][cdn];
		if (!row.customer){
			return;
		}
		dontmanage.call({
			method: 'dontmanageerp.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts.get_customer_emails',
			args: {
				'customer_name': row.customer,
				'primary_mandatory': frm.doc.primary_mandatory
			},
			callback: function(r){
				if(!r.exe){
					if(r.message.length){
						dontmanage.model.set_value(cdt, cdn, "primary_email", r.message[0])
						dontmanage.model.set_value(cdt, cdn, "billing_email", r.message[1])
					}
					else {
						return
					}
				}
			}
		})
	}
});
