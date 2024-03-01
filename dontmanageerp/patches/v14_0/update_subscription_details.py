import dontmanage


def execute():
	subscription_invoices = dontmanage.get_all(
		"Subscription Invoice", fields=["document_type", "invoice", "parent"]
	)

	for subscription_invoice in subscription_invoices:
		dontmanage.db.set_value(
			subscription_invoice.document_type,
			subscription_invoice.invoice,
			"subscription",
			subscription_invoice.parent,
		)

	dontmanage.delete_doc_if_exists("DocType", "Subscription Invoice")
