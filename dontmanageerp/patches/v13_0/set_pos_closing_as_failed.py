import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "pos_closing_entry")

	dontmanage.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
