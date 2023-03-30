# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.setup.install import create_default_cash_flow_mapper_templates


def execute():
	dontmanage.reload_doc("accounts", "doctype", dontmanage.scrub("Cash Flow Mapping"))
	dontmanage.reload_doc("accounts", "doctype", dontmanage.scrub("Cash Flow Mapper"))
	dontmanage.reload_doc("accounts", "doctype", dontmanage.scrub("Cash Flow Mapping Template Details"))

	create_default_cash_flow_mapper_templates()
