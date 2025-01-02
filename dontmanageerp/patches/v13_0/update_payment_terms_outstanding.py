# Copyright (c) 2020, DontManage and Contributors
# MIT License. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "Payment Schedule")
	if dontmanage.db.count("Payment Schedule"):
		dontmanage.db.sql(
			"""
			UPDATE
				`tabPayment Schedule` ps
			SET
				ps.outstanding = (ps.payment_amount - ps.paid_amount)
		"""
		)
