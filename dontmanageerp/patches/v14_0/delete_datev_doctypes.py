import dontmanage


def execute():
	install_apps = dontmanage.get_installed_apps()
	if "dontmanageerp_datev_uo" in install_apps or "dontmanageerp_datev" in install_apps:
		return

	# doctypes
	dontmanage.delete_doc("DocType", "DATEV Settings", ignore_missing=True, force=True)

	# reports
	dontmanage.delete_doc("Report", "DATEV", ignore_missing=True, force=True)
