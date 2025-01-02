# Copyright (c) 2015, DontManage and Contributors
# See license.txt

import unittest

import dontmanage

test_records = dontmanage.get_test_records("Operation")


class TestOperation(unittest.TestCase):
	pass


def make_operation(*args, **kwargs):
	args = args if args else kwargs
	if isinstance(args, tuple):
		args = args[0]

	args = dontmanage._dict(args)

	if not dontmanage.db.exists("Operation", args.operation):
		doc = dontmanage.get_doc(
			{"doctype": "Operation", "name": args.operation, "workstation": args.workstation}
		)
		doc.insert()
		return doc

	return dontmanage.get_doc("Operation", args.operation)
