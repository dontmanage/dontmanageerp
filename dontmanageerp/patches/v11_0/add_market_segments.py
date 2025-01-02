import dontmanage

from dontmanageerp.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	dontmanage.reload_doc("crm", "doctype", "market_segment")

	dontmanage.local.lang = dontmanage.db.get_default("lang") or "en"

	add_market_segments()
