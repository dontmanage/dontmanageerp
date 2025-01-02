import dontmanage
from dontmanage.utils import cint


def execute():
	dontmanage.reload_doc("dontmanageerp_integrations", "doctype", "woocommerce_settings")
	doc = dontmanage.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
