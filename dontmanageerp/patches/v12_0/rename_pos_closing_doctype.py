# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.table_exists("POS Closing Voucher"):
		if not dontmanage.db.exists("DocType", "POS Closing Entry"):
			dontmanage.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not dontmanage.db.exists("DocType", "POS Closing Entry Taxes"):
			dontmanage.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not dontmanage.db.exists("DocType", "POS Closing Voucher Details"):
			dontmanage.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		dontmanage.reload_doc("Accounts", "doctype", "POS Closing Entry")
		dontmanage.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		dontmanage.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if dontmanage.db.exists("DocType", "POS Closing Voucher"):
		dontmanage.delete_doc("DocType", "POS Closing Voucher")
		dontmanage.delete_doc("DocType", "POS Closing Voucher Taxes")
		dontmanage.delete_doc("DocType", "POS Closing Voucher Details")
		dontmanage.delete_doc("DocType", "POS Closing Voucher Invoices")
