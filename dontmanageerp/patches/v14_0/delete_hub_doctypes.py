import dontmanage


def execute():

	doctypes = dontmanage.get_all("DocType", {"module": "Hub Node", "custom": 0}, pluck="name")
	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True)

	dontmanage.delete_doc("Module Def", "Hub Node", ignore_missing=True, force=True)
