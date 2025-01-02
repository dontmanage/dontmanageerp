import dontmanage


def execute():
	dontmanage.reload_doc("setup", "doctype", "uom")

	uom = dontmanage.qb.DocType("UOM")

	(
		dontmanage.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
