import dontmanage


def execute():
	dontmanage.reload_doc("crm", "doctype", "lead")
	dontmanage.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
