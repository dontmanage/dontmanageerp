import dontmanage


def execute():

	dontmanage.reload_doc("selling", "doctype", "sales_order_item", force=True)
	dontmanage.reload_doc("buying", "doctype", "purchase_order_item", force=True)

	for doctype in ("Sales Order Item", "Purchase Order Item"):
		dontmanage.db.sql(
			"""
			UPDATE `tab{0}`
			SET against_blanket_order = 1
			WHERE ifnull(blanket_order, '') != ''
		""".format(
				doctype
			)
		)
