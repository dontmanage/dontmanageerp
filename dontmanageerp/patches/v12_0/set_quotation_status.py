import dontmanage


def execute():

	dontmanage.db.sql(
		""" UPDATE `tabQuotation` set status = 'Open'
		where docstatus = 1 and status = 'Submitted' """
	)
