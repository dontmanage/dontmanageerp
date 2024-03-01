import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "accounts_settings")

	dontmanage.db.set_single_value(
		"Accounts Settings", "automatically_process_deferred_accounting_entry", 1
	)
