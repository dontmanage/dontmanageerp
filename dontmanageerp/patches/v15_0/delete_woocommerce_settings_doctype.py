import dontmanage


def execute():
	dontmanage.delete_doc("DocType", "Woocommerce Settings", ignore_missing=True)
