// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.provide("dontmanageerp.support");

dontmanage.ui.form.on("Warranty Claim", {
	setup: function(frm) {
		frm.set_query('contact_person', dontmanageerp.queries.contact_query);
		frm.set_query('customer_address', dontmanageerp.queries.address_query);
		frm.set_query('customer', dontmanageerp.queries.customer);

		frm.add_fetch('serial_no', 'item_code', 'item_code');
		frm.add_fetch('serial_no', 'item_name', 'item_name');
		frm.add_fetch('serial_no', 'description', 'description');
		frm.add_fetch('serial_no', 'maintenance_status', 'warranty_amc_status');
		frm.add_fetch('serial_no', 'warranty_expiry_date', 'warranty_expiry_date');
		frm.add_fetch('serial_no', 'amc_expiry_date', 'amc_expiry_date');
		frm.add_fetch('serial_no', 'customer', 'customer');
		frm.add_fetch('serial_no', 'customer_name', 'customer_name');
		frm.add_fetch('item_code', 'item_name', 'item_name');
		frm.add_fetch('item_code', 'description', 'description');
	},
	onload: function(frm) {
		if(!frm.doc.status) {
			frm.set_value('status', 'Open');
		}
	},
	customer: function(frm) {
		dontmanageerp.utils.get_party_details(frm);
	},
	customer_address: function(frm) {
		dontmanageerp.utils.get_address_display(frm);
	},
	contact_person: function(frm) {
		dontmanageerp.utils.get_contact_details(frm);
	}
});

dontmanageerp.support.WarrantyClaim = class WarrantyClaim extends dontmanage.ui.form.Controller {
	refresh() {
		dontmanage.dynamic_link = {doc: this.frm.doc, fieldname: 'customer', doctype: 'Customer'}

		if(!cur_frm.doc.__islocal &&
			(cur_frm.doc.status=='Open' || cur_frm.doc.status == 'Work In Progress')) {
			cur_frm.add_custom_button(__('Maintenance Visit'),
				this.make_maintenance_visit);
		}
	}

	make_maintenance_visit() {
		dontmanage.model.open_mapped_doc({
			method: "dontmanageerp.support.doctype.warranty_claim.warranty_claim.make_maintenance_visit",
			frm: cur_frm
		})
	}
};

extend_cscript(cur_frm.cscript, new dontmanageerp.support.WarrantyClaim({frm: cur_frm}));

cur_frm.fields_dict['serial_no'].get_query = function(doc, cdt, cdn) {
	var cond = [];
	var filter = [
		['Serial No', 'docstatus', '!=', 2]
	];
	if(doc.item_code) {
		cond = ['Serial No', 'item_code', '=', doc.item_code];
		filter.push(cond);
	}
	if(doc.customer) {
		cond = ['Serial No', 'customer', '=', doc.customer];
		filter.push(cond);
	}
	return{
		filters:filter
	}
}

cur_frm.fields_dict['item_code'].get_query = function(doc, cdt, cdn) {
	if(doc.serial_no) {
		return{
			doctype: "Serial No",
			fields: "item_code",
			filters:{
				name: doc.serial_no
			}
		}
	}
	else{
		return{
			filters:[
				['Item', 'docstatus', '!=', 2],
				['Item', 'disabled', '=', 0]
			]
		}
	}
};
