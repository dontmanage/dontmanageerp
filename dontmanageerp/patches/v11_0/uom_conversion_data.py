import dontmanage


def execute():
	from dontmanageerp.setup.setup_wizard.operations.install_fixtures import add_uom_data

	dontmanage.reload_doc("setup", "doctype", "UOM Conversion Factor")
	dontmanage.reload_doc("setup", "doctype", "UOM")
	dontmanage.reload_doc("stock", "doctype", "UOM Category")

	if not dontmanage.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		dontmanage.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			dontmanage.delete_doc("UOM", "Hundredweight")
			dontmanage.delete_doc("UOM", "Pound Cubic Yard")
		except dontmanage.LinkExistsError:
			pass

		add_uom_data()
