# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	doctypes = [
		"Bank Statement Settings",
		"Bank Statement Settings Item",
		"Bank Statement Transaction Entry",
		"Bank Statement Transaction Invoice Item",
		"Bank Statement Transaction Payment Item",
		"Bank Statement Transaction Settings Item",
		"Bank Statement Transaction Settings",
	]

	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, force=1)

	dontmanage.delete_doc("Page", "bank-reconciliation", force=1)

	dontmanage.reload_doc("accounts", "doctype", "bank_transaction")

	rename_field("Bank Transaction", "debit", "deposit")
	rename_field("Bank Transaction", "credit", "withdrawal")
