# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import dontmanage

test_ignore = ["Leave Block List"]


class TestDepartment(unittest.TestCase):
	def test_remove_department_data(self):
		doc = create_department("Test Department")
		dontmanage.delete_doc("Department", doc.name)


def create_department(department_name, parent_department=None):
	doc = dontmanage.get_doc(
		{
			"doctype": "Department",
			"is_group": 0,
			"parent_department": parent_department,
			"department_name": department_name,
			"company": dontmanage.defaults.get_defaults().company,
		}
	).insert()

	return doc


test_records = dontmanage.get_test_records("Department")
