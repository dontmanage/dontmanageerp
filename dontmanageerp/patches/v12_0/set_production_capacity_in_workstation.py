import dontmanage


def execute():
	dontmanage.reload_doc("manufacturing", "doctype", "workstation")

	dontmanage.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
