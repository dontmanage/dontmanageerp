import dontmanage


def execute():
	# nosemgrep
	dontmanage.db.sql(
		"""
		DELETE FROM `tabAsset Movement Item`
		WHERE parent NOT IN (SELECT name FROM `tabAsset Movement`)
		"""
	)
