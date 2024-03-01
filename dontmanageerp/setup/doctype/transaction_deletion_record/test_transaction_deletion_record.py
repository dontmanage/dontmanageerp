# Copyright (c) 2021, DontManage and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestTransactionDeletionRecord(DontManageTestCase):
	def setUp(self):
		create_company("Dunder Mifflin Paper Co")

	def tearDown(self):
		dontmanage.db.rollback()

	def test_doctypes_contain_company_field(self):
		tdr = create_transaction_deletion_doc("Dunder Mifflin Paper Co")
		for doctype in tdr.doctypes:
			contains_company = False
			doctype_fields = dontmanage.get_meta(doctype.doctype_name).as_dict()["fields"]
			for doctype_field in doctype_fields:
				if doctype_field["fieldtype"] == "Link" and doctype_field["options"] == "Company":
					contains_company = True
					break
			self.assertTrue(contains_company)

	def test_no_of_docs_is_correct(self):
		for i in range(5):
			create_task("Dunder Mifflin Paper Co")
		tdr = create_transaction_deletion_doc("Dunder Mifflin Paper Co")
		for doctype in tdr.doctypes:
			if doctype.doctype_name == "Task":
				self.assertEqual(doctype.no_of_docs, 5)

	def test_deletion_is_successful(self):
		create_task("Dunder Mifflin Paper Co")
		create_transaction_deletion_doc("Dunder Mifflin Paper Co")
		tasks_containing_company = dontmanage.get_all("Task", filters={"company": "Dunder Mifflin Paper Co"})
		self.assertEqual(tasks_containing_company, [])

	def test_company_transaction_deletion_request(self):
		from dontmanageerp.setup.doctype.company.company import create_transaction_deletion_request

		# don't reuse below company for other test cases
		company = "Deep Space Exploration"
		create_company(company)

		# below call should not raise any exceptions or throw errors
		create_transaction_deletion_request(company)


def create_company(company_name):
	company = dontmanage.get_doc(
		{"doctype": "Company", "company_name": company_name, "default_currency": "INR"}
	)
	company.insert(ignore_if_duplicate=True)


def create_transaction_deletion_doc(company):
	tdr = dontmanage.get_doc({"doctype": "Transaction Deletion Record", "company": company})
	tdr.insert()
	tdr.submit()
	return tdr


def create_task(company):
	task = dontmanage.get_doc({"doctype": "Task", "company": company, "subject": "Delete"})
	task.insert()