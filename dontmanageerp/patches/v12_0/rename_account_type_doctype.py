import dontmanage


def execute():
	dontmanage.rename_doc("DocType", "Account Type", "Bank Account Type", force=True)
	dontmanage.rename_doc("DocType", "Account Subtype", "Bank Account Subtype", force=True)
	dontmanage.reload_doc("accounts", "doctype", "bank_account")
