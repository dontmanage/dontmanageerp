# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Scheduling Tool"):
		dontmanage.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
