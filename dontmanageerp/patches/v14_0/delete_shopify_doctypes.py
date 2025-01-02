import dontmanage


def execute():
	dontmanage.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	dontmanage.delete_doc("DocType", "Shopify Log", ignore_missing=True)
