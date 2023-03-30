// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

// searches for enabled users
dontmanage.provide("dontmanageerp.queries");
$.extend(dontmanageerp.queries, {
	user: function() {
		return { query: "dontmanage.core.doctype.user.user.user_query" };
	},

	lead: function() {
		return { query: "dontmanageerp.controllers.queries.lead_query" };
	},

	customer: function() {
		return { query: "dontmanageerp.controllers.queries.customer_query" };
	},

	supplier: function() {
		return { query: "dontmanageerp.controllers.queries.supplier_query" };
	},

	item: function(filters) {
		var args = { query: "dontmanageerp.controllers.queries.item_query" };
		if(filters) args["filters"] = filters;
		return args;
	},

	bom: function() {
		return { query: "dontmanageerp.controllers.queries.bom" };
	},

	task: function() {
		return { query: "dontmanageerp.projects.utils.query_task" };
	},

	customer_filter: function(doc) {
		if(!doc.customer) {
			dontmanage.throw(__("Please set {0}", [__(dontmanage.meta.get_label(doc.doctype, "customer", doc.name))]));
		}

		return { filters: { customer: doc.customer } };
	},

	contact_query: function(doc) {
		if(dontmanage.dynamic_link) {
			if(!doc[dontmanage.dynamic_link.fieldname]) {
				dontmanage.throw(__("Please set {0}",
					[__(dontmanage.meta.get_label(doc.doctype, dontmanage.dynamic_link.fieldname, doc.name))]));
			}

			return {
				query: 'dontmanage.contacts.doctype.contact.contact.contact_query',
				filters: {
					link_doctype: dontmanage.dynamic_link.doctype,
					link_name: doc[dontmanage.dynamic_link.fieldname]
				}
			};
		}
	},

	address_query: function(doc) {
		if(dontmanage.dynamic_link) {
			if(!doc[dontmanage.dynamic_link.fieldname]) {
				dontmanage.throw(__("Please set {0}",
					[__(dontmanage.meta.get_label(doc.doctype, dontmanage.dynamic_link.fieldname, doc.name))]));
			}

			return {
				query: 'dontmanage.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: dontmanage.dynamic_link.doctype,
					link_name: doc[dontmanage.dynamic_link.fieldname]
				}
			};
		}
	},

	company_address_query: function(doc) {
		return {
			query: 'dontmanage.contacts.doctype.address.address.address_query',
			filters: { is_your_company_address: 1, link_doctype: 'Company', link_name: doc.company || '' }
		};
	},

	dispatch_address_query: function(doc) {
		return {
			query: 'dontmanage.contacts.doctype.address.address.address_query',
			filters: { link_doctype: 'Company', link_name: doc.company || '' }
		};
	},

	supplier_filter: function(doc) {
		if(!doc.supplier) {
			dontmanage.throw(__("Please set {0}", [__(dontmanage.meta.get_label(doc.doctype, "supplier", doc.name))]));
		}

		return { filters: { supplier: doc.supplier } };
	},

	lead_filter: function(doc) {
		if(!doc.lead) {
			dontmanage.throw(__("Please specify a {0}",
				[__(dontmanage.meta.get_label(doc.doctype, "lead", doc.name))]));
		}

		return { filters: { lead: doc.lead } };
	},

	not_a_group_filter: function() {
		return { filters: { is_group: 0 } };
	},

	employee: function() {
		return { query: "dontmanageerp.controllers.queries.employee_query" }
	},

	warehouse: function(doc) {
		return {
			filters: [
				["Warehouse", "company", "in", ["", cstr(doc.company)]],
				["Warehouse", "is_group", "=",0]

			]
		};
	},

	get_filtered_dimensions: function(doc, child_fields, dimension, company) {
		let account = '';

		child_fields.forEach((field) => {
			if (!account) {
				account = doc[field];
			}
		});

		return {
			query: "dontmanageerp.controllers.queries.get_filtered_dimensions",
			filters: {
				'dimension': dimension,
				'account': account,
				'company': company
			}
		};
	}
});

dontmanageerp.queries.setup_queries = function(frm, options, query_fn) {
	var me = this;
	var set_query = function(doctype, parentfield) {
		var link_fields = dontmanage.meta.get_docfields(doctype, frm.doc.name,
			{"fieldtype": "Link", "options": options});
		$.each(link_fields, function(i, df) {
			if(parentfield) {
				frm.set_query(df.fieldname, parentfield, query_fn);
			} else {
				frm.set_query(df.fieldname, query_fn);
			}
		});
	};

	set_query(frm.doc.doctype);

	// warehouse field in tables
	$.each(dontmanage.meta.get_docfields(frm.doc.doctype, frm.doc.name, {"fieldtype": "Table"}),
		function(i, df) {
			set_query(df.options, df.fieldname);
		});
}

/* 	if item code is selected in child table
	then list down warehouses with its quantity
	else apply default filters.
*/
dontmanageerp.queries.setup_warehouse_query = function(frm){
	frm.set_query('warehouse', 'items', function(doc, cdt, cdn) {
		var row  = locals[cdt][cdn];
		var filters = dontmanageerp.queries.warehouse(frm.doc);
		if(row.item_code){
			$.extend(filters, {"query":"dontmanageerp.controllers.queries.warehouse_query"});
			filters["filters"].push(["Bin", "item_code", "=", row.item_code]);
		}
		return filters
	});
}
