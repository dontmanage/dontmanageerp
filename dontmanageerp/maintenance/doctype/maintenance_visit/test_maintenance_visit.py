# Copyright (c) 2015, DontManage and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.utils.data import today

# test_records = dontmanage.get_test_records('Maintenance Visit')


class TestMaintenanceVisit(unittest.TestCase):
	pass


def make_maintenance_visit():
	mv = dontmanage.new_doc("Maintenance Visit")
	mv.company = "_Test Company"
	mv.customer = "_Test Customer"
	mv.mntc_date = today()
	mv.completion_status = "Partially Completed"

	sales_person = make_sales_person("Dwight Schrute")

	mv.append(
		"purposes",
		{
			"item_code": "_Test Item",
			"sales_person": "Sales Team",
			"description": "Test Item",
			"work_done": "Test Work Done",
			"service_person": sales_person.name,
		},
	)
	mv.insert(ignore_permissions=True)

	return mv


def make_sales_person(name):
	sales_person = dontmanage.get_doc({"doctype": "Sales Person", "sales_person_name": name})
	sales_person.insert(ignore_if_duplicate=True)

	return sales_person
