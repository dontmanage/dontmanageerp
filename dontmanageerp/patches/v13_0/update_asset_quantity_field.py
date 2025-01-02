import dontmanage


def execute():
	if dontmanage.db.count("Asset"):
		dontmanage.reload_doc("assets", "doctype", "Asset")
		asset = dontmanage.qb.DocType("Asset")
		dontmanage.qb.update(asset).set(asset.asset_quantity, 1).run()
