# Copyright (c) 2023, DontManage and Contributors
# License: MIT. See LICENSE


import dontmanage

from dontmanageerp import get_default_company


def execute():
	company = get_default_company()
	if company:
		for d in dontmanage.get_all("Lower Deduction Certificate", pluck="name"):
			dontmanage.db.set_value("Lower Deduction Certificate", d, "company", company, update_modified=False)
