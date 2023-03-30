# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():

	dontmanage.reload_doc("accounts", "doctype", "subscription")
	dontmanage.reload_doc("accounts", "doctype", "subscription_invoice")
	dontmanage.reload_doc("accounts", "doctype", "subscription_plan")

	if dontmanage.db.has_column("Subscription", "customer"):
		dontmanage.db.sql(
			"""
			UPDATE `tabSubscription`
			SET
				start_date = start,
				party_type = 'Customer',
				party = customer,
				sales_tax_template = tax_template
			WHERE IFNULL(party,'') = ''
		"""
		)

	dontmanage.db.sql(
		"""
		UPDATE `tabSubscription Invoice`
		SET document_type = 'Sales Invoice'
		WHERE IFNULL(document_type, '') = ''
	"""
	)

	price_determination_map = {
		"Fixed rate": "Fixed Rate",
		"Based on price list": "Based On Price List",
	}

	for key, value in price_determination_map.items():
		dontmanage.db.sql(
			"""
			UPDATE `tabSubscription Plan`
			SET price_determination = %s
			WHERE price_determination = %s
		""",
			(value, key),
		)
