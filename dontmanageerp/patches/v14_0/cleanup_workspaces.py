import dontmanage


def execute():
	for ws in ["Retail", "Utilities"]:
		dontmanage.delete_doc_if_exists("Workspace", ws)

	for ws in ["Integrations", "Settings"]:
		dontmanage.db.set_value("Workspace", ws, "public", 0)
