# Copyright (c) 2013, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.query_builder.functions import Sum


def execute(filters=None):

	if not filters:
		filters = {}
	columns = get_columns(filters)
	stock = get_total_stock(filters)

	return columns, stock


def get_columns(filters):
	columns = [
		_("Item") + ":Link/Item:150",
		_("Description") + "::300",
		_("Current Qty") + ":Float:100",
	]

	if filters.get("group_by") == "Warehouse":
		columns.insert(0, _("Warehouse") + ":Link/Warehouse:150")
	else:
		columns.insert(0, _("Company") + ":Link/Company:250")

	return columns


def get_total_stock(filters):
	bin = dontmanage.qb.DocType("Bin")
	item = dontmanage.qb.DocType("Item")
	wh = dontmanage.qb.DocType("Warehouse")

	query = (
		dontmanage.qb.from_(bin)
		.inner_join(item)
		.on(bin.item_code == item.item_code)
		.inner_join(wh)
		.on(wh.name == bin.warehouse)
		.where(bin.actual_qty != 0)
	)

	if filters.get("group_by") == "Warehouse":
		if filters.get("company"):
			query = query.where(wh.company == filters.get("company"))

		query = query.select(bin.warehouse).groupby(bin.warehouse)
	else:
		query = query.select(wh.company).groupby(wh.company)

	query = query.select(
		item.item_code, item.description, Sum(bin.actual_qty).as_("actual_qty")
	).groupby(item.item_code)

	return query.run()
