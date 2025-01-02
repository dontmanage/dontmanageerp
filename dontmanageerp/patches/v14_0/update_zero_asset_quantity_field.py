import dontmanage


def execute():
	asset = dontmanage.qb.DocType("Asset")
	dontmanage.qb.update(asset).set(asset.asset_quantity, 1).where(asset.asset_quantity == 0).run()
