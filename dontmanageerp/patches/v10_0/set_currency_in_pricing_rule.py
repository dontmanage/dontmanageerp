import dontmanage


def execute():
	dontmanage.reload_doctype("Pricing Rule")

	currency = dontmanage.db.get_default("currency")
	for doc in dontmanage.get_all("Pricing Rule", fields=["company", "name"]):
		if doc.company:
			currency = dontmanage.get_cached_value("Company", doc.company, "default_currency")

		dontmanage.db.sql(
			"""update `tabPricing Rule` set currency = %s where name = %s""", (currency, doc.name)
		)
