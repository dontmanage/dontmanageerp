import dontmanage


def execute():
	if "agriculture" in dontmanage.get_installed_apps():
		return

	dontmanage.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)

	dontmanage.delete_doc("Workspace", "Agriculture", ignore_missing=True, force=True)

	reports = dontmanage.get_all("Report", {"module": "agriculture", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		dontmanage.delete_doc("Report", report, ignore_missing=True, force=True)

	dashboards = dontmanage.get_all(
		"Dashboard", {"module": "agriculture", "is_standard": 1}, pluck="name"
	)
	for dashboard in dashboards:
		dontmanage.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	doctypes = dontmanage.get_all("DocType", {"module": "agriculture", "custom": 0}, pluck="name")
	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True)

	dontmanage.delete_doc("Module Def", "Agriculture", ignore_missing=True, force=True)
