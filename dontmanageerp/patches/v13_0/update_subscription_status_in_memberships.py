import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Member"):
		dontmanage.reload_doc("Non Profit", "doctype", "Member")

		if dontmanage.db.has_column("Member", "subscription_activated"):
			dontmanage.db.sql(
				'UPDATE `tabMember` SET subscription_status = "Active" WHERE subscription_activated = 1'
			)
			dontmanage.db.sql_ddl("ALTER table `tabMember` DROP COLUMN subscription_activated")
