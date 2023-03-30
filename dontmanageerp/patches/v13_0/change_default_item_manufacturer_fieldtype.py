import dontmanage


def execute():

	# Erase all default item manufacturers that dont exist.
	item = dontmanage.qb.DocType("Item")
	manufacturer = dontmanage.qb.DocType("Manufacturer")

	(
		dontmanage.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
