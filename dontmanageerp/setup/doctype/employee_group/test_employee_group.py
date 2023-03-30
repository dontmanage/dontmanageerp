# Copyright (c) 2018, DontManage and Contributors
# See license.txt

import unittest

import dontmanage

from dontmanageerp.setup.doctype.employee.test_employee import make_employee


class TestEmployeeGroup(unittest.TestCase):
	pass


def make_employee_group():
	employee = make_employee("testemployee@example.com")
	employee_group = dontmanage.get_doc(
		{
			"doctype": "Employee Group",
			"employee_group_name": "_Test Employee Group",
			"employee_list": [{"employee": employee}],
		}
	)
	employee_group_exist = dontmanage.db.exists("Employee Group", "_Test Employee Group")
	if not employee_group_exist:
		employee_group.insert()
		return employee_group.employee_group_name
	else:
		return employee_group_exist


def get_employee_group():
	employee_group = dontmanage.db.exists("Employee Group", "_Test Employee Group")
	return employee_group
