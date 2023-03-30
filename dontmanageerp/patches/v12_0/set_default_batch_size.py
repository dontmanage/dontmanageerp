import dontmanage


def execute():
	dontmanage.reload_doc("manufacturing", "doctype", "bom_operation")
	dontmanage.reload_doc("manufacturing", "doctype", "work_order_operation")

	dontmanage.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	dontmanage.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
