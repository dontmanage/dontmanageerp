import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "accounts_settings")

	dontmanage.db.set_value(
		"Accounts Settings", None, "automatically_process_deferred_accounting_entry", 1
	)
