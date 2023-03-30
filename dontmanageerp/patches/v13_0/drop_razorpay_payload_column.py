import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Membership"):
		if "webhook_payload" in dontmanage.db.get_table_columns("Membership"):
			dontmanage.db.sql("alter table `tabMembership` drop column webhook_payload")
