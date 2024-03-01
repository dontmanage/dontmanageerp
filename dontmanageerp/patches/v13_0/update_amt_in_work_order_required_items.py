import dontmanage


def execute():
	"""Correct amount in child table of required items table."""

	dontmanage.reload_doc("manufacturing", "doctype", "work_order")
	dontmanage.reload_doc("manufacturing", "doctype", "work_order_item")

	dontmanage.db.sql(
		"""UPDATE `tabWork Order Item` SET amount = ifnull(rate, 0.0) * ifnull(required_qty, 0.0)"""
	)
