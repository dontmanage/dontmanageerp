# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage

# test_records = dontmanage.get_test_records('Designation')


def create_designation(**args):
	args = dontmanage._dict(args)
	if dontmanage.db.exists("Designation", args.designation_name or "_Test designation"):
		return dontmanage.get_doc("Designation", args.designation_name or "_Test designation")

	designation = dontmanage.get_doc(
		{
			"doctype": "Designation",
			"designation_name": args.designation_name or "_Test designation",
			"description": args.description or "_Test description",
		}
	)
	designation.save()
	return designation
