# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.table_exists("Bank Reconciliation"):
		dontmanage.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		dontmanage.reload_doc("Accounts", "doctype", "Bank Clearance")

		dontmanage.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		dontmanage.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
