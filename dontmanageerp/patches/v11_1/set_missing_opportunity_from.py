import dontmanage


def execute():

	dontmanage.reload_doctype("Opportunity")
	if dontmanage.db.has_column("Opportunity", "enquiry_from"):
		dontmanage.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if dontmanage.db.has_column("Opportunity", "lead") and dontmanage.db.has_column(
		"Opportunity", "enquiry_from"
	):
		dontmanage.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if dontmanage.db.has_column("Opportunity", "customer") and dontmanage.db.has_column(
		"Opportunity", "enquiry_from"
	):
		dontmanage.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
