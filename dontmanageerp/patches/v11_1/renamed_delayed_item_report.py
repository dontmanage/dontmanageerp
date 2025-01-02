# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if dontmanage.db.exists("Report", report):
			dontmanage.delete_doc("Report", report)
