// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanageerp.accounts.taxes.setup_tax_validations("Purchase Taxes and Charges Template");
dontmanageerp.accounts.taxes.setup_tax_filters("Purchase Taxes and Charges");

dontmanage.ui.form.on("Purchase Taxes and Charges", {
	add_deduct_tax(doc, cdt, cdn) {
		let d = locals[cdt][cdn];

		if(!d.category && d.add_deduct_tax) {
			dontmanage.msgprint(__("Please select Category first"));
			d.add_deduct_tax = '';
		}
		else if(d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
			dontmanage.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
			d.add_deduct_tax = '';
		}
		refresh_field('add_deduct_tax', d.name, 'taxes');
	},

	category(doc, cdt, cdn) {
		let d = locals[cdt][cdn];

		if(d.category != 'Total' && d.add_deduct_tax == 'Deduct') {
			dontmanage.msgprint(__("Cannot deduct when category is for 'Valuation' or 'Valuation and Total'"));
			d.add_deduct_tax = '';
		}
		refresh_field('add_deduct_tax', d.name, 'taxes');
	}
});
