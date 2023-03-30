# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():

	dontmanage.reload_doc("accounts", "doctype", "bank_account")
	dontmanage.reload_doc("accounts", "doctype", "bank")

	if dontmanage.db.has_column("Bank", "branch_code") and dontmanage.db.has_column(
		"Bank Account", "branch_code"
	):
		dontmanage.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
