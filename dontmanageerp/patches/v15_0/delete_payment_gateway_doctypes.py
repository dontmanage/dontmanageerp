import dontmanage


def execute():
	for dt in ("GoCardless Settings", "GoCardless Mandate", "Mpesa Settings"):
		dontmanage.delete_doc("DocType", dt, ignore_missing=True)
