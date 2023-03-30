import dontmanage


def execute():
	from dontmanageerp.setup.setup_wizard.operations.install_fixtures import add_uom_data

	dontmanage.reload_doc("setup", "doctype", "UOM Conversion Factor")
	dontmanage.reload_doc("setup", "doctype", "UOM")
	dontmanage.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
