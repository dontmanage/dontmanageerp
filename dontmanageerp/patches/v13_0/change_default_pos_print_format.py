import dontmanage


def execute():
	dontmanage.db.sql(
		"""UPDATE `tabPOS Profile` profile
		SET profile.`print_format` = 'POS Invoice'
		WHERE profile.`print_format` = 'Point of Sale'"""
	)
