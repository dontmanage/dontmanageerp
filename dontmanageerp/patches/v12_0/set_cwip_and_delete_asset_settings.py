import dontmanage
from dontmanage.utils import cint


def execute():
	"""Get 'Disable CWIP Accounting value' from Asset Settings, set it in 'Enable Capital Work in Progress Accounting' field
	in Company, delete Asset Settings"""

	if dontmanage.db.exists("DocType", "Asset Settings"):
		dontmanage.reload_doctype("Asset Category")
		cwip_value = dontmanage.db.get_single_value("Asset Settings", "disable_cwip_accounting")

		dontmanage.db.sql("""UPDATE `tabAsset Category` SET enable_cwip_accounting = %s""", cint(cwip_value))

		dontmanage.db.sql("""DELETE FROM `tabSingles` where doctype = 'Asset Settings'""")
		dontmanage.delete_doc_if_exists("DocType", "Asset Settings")
