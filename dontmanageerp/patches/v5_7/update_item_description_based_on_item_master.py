import dontmanage


def execute():
	name = dontmanage.db.sql(
		""" select name from `tabPatch Log` \
		where \
			patch like 'execute:dontmanage.db.sql("update `tabProduction Order` pro set description%' """
	)
	if not name:
		dontmanage.db.sql(
			"update `tabProduction Order` pro \
			set \
				description = (select description from tabItem where name=pro.production_item) \
			where \
				ifnull(description, '') = ''"
		)
