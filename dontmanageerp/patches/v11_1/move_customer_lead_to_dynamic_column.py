# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doctype("Quotation")
	dontmanage.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	dontmanage.db.sql(
		""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """
	)

	dontmanage.reload_doctype("Opportunity")
	dontmanage.db.sql(
		""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """
	)
	dontmanage.db.sql(
		""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """
	)
