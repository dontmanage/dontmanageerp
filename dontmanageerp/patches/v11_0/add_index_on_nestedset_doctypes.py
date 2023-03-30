# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("assets", "doctype", "Location")
	for dt in (
		"Account",
		"Cost Center",
		"File",
		"Employee",
		"Location",
		"Task",
		"Customer Group",
		"Sales Person",
		"Territory",
	):
		dontmanage.reload_doctype(dt)
		dontmanage.get_doc("DocType", dt).run_module_method("on_doctype_update")
