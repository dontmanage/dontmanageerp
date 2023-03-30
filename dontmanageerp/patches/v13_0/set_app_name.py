import dontmanage


def execute():
	dontmanage.reload_doctype("System Settings")
	settings = dontmanage.get_doc("System Settings")
	settings.db_set("app_name", "DontManageErp", commit=True)
