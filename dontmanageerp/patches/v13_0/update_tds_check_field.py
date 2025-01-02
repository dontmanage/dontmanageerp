import dontmanage


def execute():
	if dontmanage.db.has_table("Tax Withholding Category") and dontmanage.db.has_column(
		"Tax Withholding Category", "round_off_tax_amount"
	):
		dontmanage.db.sql(
			"""
			UPDATE `tabTax Withholding Category` set round_off_tax_amount = 0
			WHERE round_off_tax_amount IS NULL
		"""
		)
