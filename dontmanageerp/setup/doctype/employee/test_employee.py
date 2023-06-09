# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import dontmanage
import dontmanage.utils

import dontmanageerp
from dontmanageerp.setup.doctype.employee.employee import InactiveEmployeeStatusError

test_records = dontmanage.get_test_records("Employee")


class TestEmployee(unittest.TestCase):
	def test_employee_status_left(self):
		employee1 = make_employee("test_employee_1@company.com")
		employee2 = make_employee("test_employee_2@company.com")
		employee1_doc = dontmanage.get_doc("Employee", employee1)
		employee2_doc = dontmanage.get_doc("Employee", employee2)
		employee2_doc.reload()
		employee2_doc.reports_to = employee1_doc.name
		employee2_doc.save()
		employee1_doc.reload()
		employee1_doc.status = "Left"
		self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)

	def tearDown(self):
		dontmanage.db.rollback()


def make_employee(user, company=None, **kwargs):
	if not dontmanage.db.get_value("User", user):
		dontmanage.get_doc(
			{
				"doctype": "User",
				"email": user,
				"first_name": user,
				"new_password": "password",
				"send_welcome_email": 0,
				"roles": [{"doctype": "Has Role", "role": "Employee"}],
			}
		).insert()

	if not dontmanage.db.get_value("Employee", {"user_id": user}):
		employee = dontmanage.get_doc(
			{
				"doctype": "Employee",
				"naming_series": "EMP-",
				"first_name": user,
				"company": company or dontmanageerp.get_default_company(),
				"user_id": user,
				"date_of_birth": "1990-05-08",
				"date_of_joining": "2013-01-01",
				"department": dontmanage.get_all("Department", fields="name")[0].name,
				"gender": "Female",
				"company_email": user,
				"prefered_contact_email": "Company Email",
				"prefered_email": user,
				"status": "Active",
				"employment_type": "Intern",
			}
		)
		if kwargs:
			employee.update(kwargs)
		employee.insert()
		return employee.name
	else:
		dontmanage.db.set_value("Employee", {"employee_name": user}, "status", "Active")
		return dontmanage.get_value("Employee", {"employee_name": user}, "name")
