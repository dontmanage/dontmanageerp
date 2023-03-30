import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "item_tax_template")

	item_tax_template_list = dontmanage.get_list("Item Tax Template")
	for template in item_tax_template_list:
		doc = dontmanage.get_doc("Item Tax Template", template.name)
		for tax in doc.taxes:
			doc.company = dontmanage.get_value("Account", tax.tax_type, "company")
			break
		doc.save()
