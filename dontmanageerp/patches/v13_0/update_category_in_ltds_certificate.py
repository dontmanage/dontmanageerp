import dontmanage


def execute():
	company = dontmanage.get_all("Company", filters={"country": "India"})
	if not company:
		return

	dontmanage.reload_doc("regional", "doctype", "lower_deduction_certificate")

	ldc = dontmanage.qb.DocType("Lower Deduction Certificate").as_("ldc")
	supplier = dontmanage.qb.DocType("Supplier")

	dontmanage.qb.update(ldc).inner_join(supplier).on(ldc.supplier == supplier.name).set(
		ldc.tax_withholding_category, supplier.tax_withholding_category
	).where(ldc.tax_withholding_category.isnull()).run()
