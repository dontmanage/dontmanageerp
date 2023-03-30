# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():

	if dontmanage.db.exists("DocType", "Bank Reconciliation Detail") and dontmanage.db.exists(
		"DocType", "Bank Clearance Detail"
	):

		dontmanage.delete_doc("DocType", "Bank Reconciliation Detail", force=1)
