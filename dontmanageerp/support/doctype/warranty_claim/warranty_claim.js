// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.provide("dontmanageerp.support");

dontmanage.ui.form.on("Warranty Claim", {
	setup: (frm) => {
		frm.set_query("contact_person", dontmanageerp.queries.contact_query);
		frm.set_query("customer_address", dontmanageerp.queries.address_query);
		frm.set_query("customer", dontmanageerp.queries.customer);

		frm.set_query("serial_no", () => {
			let filters = {
				company: frm.doc.company,
			};

			if (frm.doc.item_code) {
				filters["item_code"] = frm.doc.item_code;
			}

			return { filters: filters };
		});

		frm.set_query("item_code", () => {
			return {
				filters: {
					disabled: 0,
				},
			};
		});
	},

	onload: (frm) => {
		if (!frm.doc.status) {
			frm.set_value("status", "Open");
		}
	},

	refresh: (frm) => {
		dontmanage.dynamic_link = {
			doc: frm.doc,
			fieldname: "customer",
			doctype: "Customer",
		};

		if (
			!frm.doc.__islocal &&
			["Open", "Work In Progress"].includes(frm.doc.status)
		) {
			frm.add_custom_button(__("Maintenance Visit"), () => {
				dontmanage.model.open_mapped_doc({
					method: "dontmanageerp.support.doctype.warranty_claim.warranty_claim.make_maintenance_visit",
					frm: frm,
				});
			});
		}
	},

	customer: (frm) => {
		dontmanageerp.utils.get_party_details(frm);
	},

	customer_address: (frm) => {
		dontmanageerp.utils.get_address_display(frm);
	},

	contact_person: (frm) => {
		dontmanageerp.utils.get_contact_details(frm);
	},
});
