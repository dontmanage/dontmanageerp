import dontmanage


def execute():
	dontmanage.delete_doc("DocType", "Amazon MWS Settings", ignore_missing=True)
