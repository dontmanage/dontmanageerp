import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		dontmanage.db.table_exists("Bank")
		and dontmanage.db.table_exists("Bank Account")
		and dontmanage.db.has_column("Bank Account", "swift_number")
	):
		try:
			dontmanage.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception as e:
			dontmanage.log_error("Bank to Bank Account patch migration failed")

	dontmanage.reload_doc("accounts", "doctype", "bank_account")
	dontmanage.reload_doc("accounts", "doctype", "payment_request")
