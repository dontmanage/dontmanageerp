import dontmanage


def execute():
	dontmanage.reload_doc("manufacturing", "doctype", "work_order")

	dontmanage.db.sql(
		"""
		UPDATE
			`tabWork Order` wo
				JOIN `tabItem` item ON wo.production_item = item.item_code
		SET
			wo.item_name = item.item_name
	"""
	)
	dontmanage.db.commit()
