# Copyright (c) 2020, DontManage and Contributors
# MIT License. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "POS Invoice Merge Log")
	dontmanage.reload_doc("accounts", "doctype", "POS Closing Entry")
	if dontmanage.db.count("POS Invoice Merge Log"):
		dontmanage.db.sql(
			"""
			UPDATE
				`tabPOS Invoice Merge Log` log, `tabPOS Invoice Reference` log_ref
			SET
				log.pos_closing_entry = (
					SELECT clo_ref.parent FROM `tabPOS Invoice Reference` clo_ref
					WHERE clo_ref.pos_invoice = log_ref.pos_invoice
					AND clo_ref.parenttype = 'POS Closing Entry' LIMIT 1
				)
			WHERE
				log_ref.parent = log.name
		"""
		)

		dontmanage.db.sql("""UPDATE `tabPOS Closing Entry` SET status = 'Submitted' where docstatus = 1""")
		dontmanage.db.sql("""UPDATE `tabPOS Closing Entry` SET status = 'Cancelled' where docstatus = 2""")
