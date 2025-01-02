import dontmanage


def execute():
	dontmanage.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	dontmanage.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
