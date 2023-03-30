# Copyright (c) 2013, DontManage and contributors
# For license information, please see license.txt


import dontmanage

from dontmanageerp.projects.report.billing_summary import get_columns, get_data


def execute(filters=None):
	filters = dontmanage._dict(filters or {})
	columns = get_columns()

	data = get_data(filters)
	return columns, data
