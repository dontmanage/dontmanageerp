# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.exists("Company", {"country": "India"}):
		return

	dontmanage.reload_doc("core", "doctype", "has_role")
	dontmanage.db.sql(
		"""
		delete from
			`tabHas Role`
		where
			parenttype = 'Report' and parent in('GST Sales Register',
				'GST Purchase Register', 'GST Itemised Sales Register',
				'GST Itemised Purchase Register', 'Eway Bill')
		"""
	)
