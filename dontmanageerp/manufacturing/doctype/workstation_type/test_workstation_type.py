# Copyright (c) 2022, DontManage and Contributors
# See license.txt

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestWorkstationType(DontManageTestCase):
	pass


def create_workstation_type(**args):
	args = dontmanage._dict(args)

	if workstation_type := dontmanage.db.exists("Workstation Type", args.workstation_type):
		return dontmanage.get_doc("Workstation Type", workstation_type)
	else:
		doc = dontmanage.new_doc("Workstation Type")
		doc.update(args)
		doc.insert()
		return doc
