import dontmanage


def execute():
	dontmanage.reload_doc("stock", "doctype", "shipment")

	# update submitted status
	dontmanage.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Submitted"
					WHERE status = "Draft" AND docstatus = 1"""
	)

	# update cancelled status
	dontmanage.db.sql(
		"""UPDATE `tabShipment`
					SET status = "Cancelled"
					WHERE status = "Draft" AND docstatus = 2"""
	)
