import dontmanage


# not able to use dontmanage.qb because of this bug https://github.com/dontmanage/dontmanage/issues/20292
def execute():
	if dontmanage.db.has_column("Asset Repair", "warehouse"):
		# nosemgrep
		dontmanage.db.sql(
			"""UPDATE `tabAsset Repair Consumed Item` ar_item
			JOIN `tabAsset Repair` ar
			ON ar.name = ar_item.parent
			SET ar_item.warehouse = ar.warehouse
			WHERE ifnull(ar.warehouse, '') != ''"""
		)
