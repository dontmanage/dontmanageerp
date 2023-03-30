import click
import dontmanage


def execute():
	if "education" in dontmanage.get_installed_apps():
		return

	dontmanage.delete_doc("Workspace", "Education", ignore_missing=True, force=True)

	pages = dontmanage.get_all("Page", {"module": "education"}, pluck="name")
	for page in pages:
		dontmanage.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = dontmanage.get_all("Report", {"module": "education", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		dontmanage.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = dontmanage.get_all(
		"Print Format", {"module": "education", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		dontmanage.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	dontmanage.reload_doc("website", "doctype", "website_settings")
	forms = dontmanage.get_all("Web Form", {"module": "education", "is_standard": 1}, pluck="name")
	for form in forms:
		dontmanage.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = dontmanage.get_all("Dashboard", {"module": "education", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		dontmanage.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = dontmanage.get_all(
		"Dashboard Chart", {"module": "education", "is_standard": 1}, pluck="name"
	)
	for dashboard in dashboards:
		dontmanage.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	dontmanage.reload_doc("desk", "doctype", "number_card")
	cards = dontmanage.get_all("Number Card", {"module": "education", "is_standard": 1}, pluck="name")
	for card in cards:
		dontmanage.delete_doc("Number Card", card, ignore_missing=True, force=True)

	doctypes = dontmanage.get_all("DocType", {"module": "education", "custom": 0}, pluck="name")
	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True)

	dontmanage.delete_doc("Module Def", "Education", ignore_missing=True, force=True)

	click.secho(
		"Education Module is moved to a separate app"
		"Please install the app to continue using the module: https://github.com/dontmanage/education",
		fg="yellow",
	)
