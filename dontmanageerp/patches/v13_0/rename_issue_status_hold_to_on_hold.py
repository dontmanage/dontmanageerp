# Copyright (c) 2020, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Issue"):
		dontmanage.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	dontmanage.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
