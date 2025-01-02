import dontmanage


def execute():
	dontmanage.db.sql(
		"""UPDATE `tabUser` SET `home_settings` = REPLACE(`home_settings`, 'Accounting', 'Accounts')"""
	)
	dontmanage.cache().delete_key("home_settings")
