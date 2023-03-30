import dontmanage


def execute():
	dontmanage.reload_doc("manufacturing", "doctype", "bom")
	dontmanage.reload_doc("manufacturing", "doctype", "bom_operation")

	dontmanage.db.sql(
		"""
		UPDATE
			`tabBOM Operation`
		SET
			time_in_mins = (operating_cost * 60) / hour_rate
		WHERE
			time_in_mins = 0 AND operating_cost > 0
			AND hour_rate > 0 AND docstatus = 1 AND parenttype = "BOM"
	"""
	)
