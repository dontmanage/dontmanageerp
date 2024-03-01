import dontmanage


def execute():
	if "healthcare" in dontmanage.get_installed_apps():
		return

	dontmanage.delete_doc("Workspace", "Healthcare", ignore_missing=True, force=True)

	pages = dontmanage.get_all("Page", {"module": "healthcare"}, pluck="name")
	for page in pages:
		dontmanage.delete_doc("Page", page, ignore_missing=True, force=True)

	reports = dontmanage.get_all("Report", {"module": "healthcare", "is_standard": "Yes"}, pluck="name")
	for report in reports:
		dontmanage.delete_doc("Report", report, ignore_missing=True, force=True)

	print_formats = dontmanage.get_all(
		"Print Format", {"module": "healthcare", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		dontmanage.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	dontmanage.reload_doc("website", "doctype", "website_settings")
	forms = dontmanage.get_all("Web Form", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for form in forms:
		dontmanage.delete_doc("Web Form", form, ignore_missing=True, force=True)

	dashboards = dontmanage.get_all("Dashboard", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for dashboard in dashboards:
		dontmanage.delete_doc("Dashboard", dashboard, ignore_missing=True, force=True)

	dashboards = dontmanage.get_all(
		"Dashboard Chart", {"module": "healthcare", "is_standard": 1}, pluck="name"
	)
	for dashboard in dashboards:
		dontmanage.delete_doc("Dashboard Chart", dashboard, ignore_missing=True, force=True)

	dontmanage.reload_doc("desk", "doctype", "number_card")
	cards = dontmanage.get_all("Number Card", {"module": "healthcare", "is_standard": 1}, pluck="name")
	for card in cards:
		dontmanage.delete_doc("Number Card", card, ignore_missing=True, force=True)

	titles = ["Lab Test", "Prescription", "Patient Appointment", "Patient"]
	items = dontmanage.get_all("Portal Menu Item", filters=[["title", "in", titles]], pluck="name")
	for item in items:
		dontmanage.delete_doc("Portal Menu Item", item, ignore_missing=True, force=True)

	doctypes = dontmanage.get_all("DocType", {"module": "healthcare", "custom": 0}, pluck="name")
	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True)

	dontmanage.delete_doc("Module Def", "Healthcare", ignore_missing=True, force=True)

	custom_fields = {
		"Sales Invoice": ["patient", "patient_name", "ref_practitioner"],
		"Sales Invoice Item": ["reference_dt", "reference_dn"],
		"Stock Entry": ["inpatient_medication_entry"],
		"Stock Entry Detail": ["patient", "inpatient_medication_entry_child"],
	}
	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = dontmanage.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			dontmanage.delete_doc("Custom Field", record, ignore_missing=True, force=True)
