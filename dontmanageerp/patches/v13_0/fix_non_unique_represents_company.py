import dontmanage


def execute():
	dontmanage.db.sql(
		"""
		update tabCustomer
		set represents_company = NULL
		where represents_company = ''
	"""
	)
