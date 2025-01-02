import dontmanage


def execute():
	dontmanage.reload_doc("projects", "doctype", "project")

	dontmanage.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
