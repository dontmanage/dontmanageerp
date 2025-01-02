# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	dontmanage.reload_doc("projects", "doctype", "project")

	if dontmanage.db.has_column("Project", "from"):
		rename_field("Project", "from", "from_time")
		rename_field("Project", "to", "to_time")
