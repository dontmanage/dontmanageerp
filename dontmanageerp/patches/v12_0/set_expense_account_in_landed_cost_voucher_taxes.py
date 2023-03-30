import dontmanage


def execute():
	dontmanage.reload_doctype("Landed Cost Taxes and Charges")

	company_account_map = dontmanage._dict(
		dontmanage.db.sql(
			"""
		SELECT name, expenses_included_in_valuation from `tabCompany`
	"""
		)
	)

	for company, account in company_account_map.items():
		dontmanage.db.sql(
			"""
			UPDATE
				`tabLanded Cost Taxes and Charges` t, `tabLanded Cost Voucher` l
			SET
				t.expense_account = %s
			WHERE
				l.docstatus = 1
				AND l.company = %s
				AND t.parent = l.name
		""",
			(account, company),
		)

		dontmanage.db.sql(
			"""
			UPDATE
				`tabLanded Cost Taxes and Charges` t, `tabStock Entry` s
			SET
				t.expense_account = %s
			WHERE
				s.docstatus = 1
				AND s.company = %s
				AND t.parent = s.name
		""",
			(account, company),
		)
