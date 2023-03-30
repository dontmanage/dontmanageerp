import dontmanage

from dontmanageerp.setup.setup_wizard.operations.install_fixtures import add_sale_stages


def execute():
	dontmanage.reload_doc("crm", "doctype", "sales_stage")

	dontmanage.local.lang = dontmanage.db.get_default("lang") or "en"

	add_sale_stages()
