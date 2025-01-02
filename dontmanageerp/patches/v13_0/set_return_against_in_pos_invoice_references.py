import dontmanage


def execute():
	"""
	Fetch and Set is_return & return_against from POS Invoice in POS Invoice References table.
	"""

	POSClosingEntry = dontmanage.qb.DocType("POS Closing Entry")
	open_pos_closing_entries = (
		dontmanage.qb.from_(POSClosingEntry)
		.select(POSClosingEntry.name)
		.where(POSClosingEntry.docstatus == 0)
		.run(pluck=True)
	)

	if not open_pos_closing_entries:
		return

	POSInvoiceReference = dontmanage.qb.DocType("POS Invoice Reference")
	POSInvoice = dontmanage.qb.DocType("POS Invoice")
	pos_invoice_references = (
		dontmanage.qb.from_(POSInvoiceReference)
		.join(POSInvoice)
		.on(POSInvoiceReference.pos_invoice == POSInvoice.name)
		.select(POSInvoiceReference.name, POSInvoice.is_return, POSInvoice.return_against)
		.where(POSInvoiceReference.parent.isin(open_pos_closing_entries))
		.run(as_dict=True)
	)

	for row in pos_invoice_references:
		dontmanage.db.set_value("POS Invoice Reference", row.name, "is_return", row.is_return)
		if row.is_return:
			dontmanage.db.set_value("POS Invoice Reference", row.name, "return_against", row.return_against)
		else:
			dontmanage.db.set_value("POS Invoice Reference", row.name, "return_against", None)
