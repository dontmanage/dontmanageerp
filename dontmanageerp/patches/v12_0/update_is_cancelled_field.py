import dontmanage


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not dontmanage.db.has_column(doctype, "is_cancelled")
			or dontmanage.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		dontmanage.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL""".format(
				doctype=doctype
			)
		)
		dontmanage.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'""".format(
				doctype=doctype
			)
		)

		dontmanage.reload_doc(module, "doctype", dontmanage.scrub(doctype))
