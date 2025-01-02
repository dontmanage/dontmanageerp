import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "tax_category")
	dontmanage.reload_doc("stock", "doctype", "item_manufacturer")
	company = dontmanage.get_all("Company", filters={"country": "India"})
	if not company:
		return
	if dontmanage.db.exists("Custom Field", "Company-bank_remittance_section"):
		deprecated_fields = [
			"bank_remittance_section",
			"client_code",
			"remittance_column_break",
			"product_code",
		]
		for i in range(len(deprecated_fields)):
			dontmanage.delete_doc("Custom Field", "Company-" + deprecated_fields[i])
