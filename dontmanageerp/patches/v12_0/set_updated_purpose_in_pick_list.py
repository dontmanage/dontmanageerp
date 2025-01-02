# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("stock", "doctype", "pick_list")
	dontmanage.db.sql(
		"""UPDATE `tabPick List` set purpose = 'Delivery'
        WHERE docstatus = 1  and purpose = 'Delivery against Sales Order' """
	)
