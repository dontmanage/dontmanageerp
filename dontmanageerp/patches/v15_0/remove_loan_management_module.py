import dontmanage


def execute():
	if "lending" in dontmanage.get_installed_apps():
		return

	dontmanage.delete_doc("Module Def", "Loan Management", ignore_missing=True, force=True)

	dontmanage.delete_doc("Workspace", "Loans", ignore_missing=True, force=True)

	print_formats = dontmanage.get_all(
		"Print Format", {"module": "Loan Management", "standard": "Yes"}, pluck="name"
	)
	for print_format in print_formats:
		dontmanage.delete_doc("Print Format", print_format, ignore_missing=True, force=True)

	reports = dontmanage.get_all(
		"Report", {"module": "Loan Management", "is_standard": "Yes"}, pluck="name"
	)
	for report in reports:
		dontmanage.delete_doc("Report", report, ignore_missing=True, force=True)

	doctypes = dontmanage.get_all("DocType", {"module": "Loan Management", "custom": 0}, pluck="name")
	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True, force=True)

	notifications = dontmanage.get_all(
		"Notification", {"module": "Loan Management", "is_standard": 1}, pluck="name"
	)
	for notifcation in notifications:
		dontmanage.delete_doc("Notification", notifcation, ignore_missing=True, force=True)

	for dt in ["Web Form", "Dashboard", "Dashboard Chart", "Number Card"]:
		records = dontmanage.get_all(dt, {"module": "Loan Management", "is_standard": 1}, pluck="name")
		for record in records:
			dontmanage.delete_doc(dt, record, ignore_missing=True, force=True)

	custom_fields = {
		"Loan": ["repay_from_salary"],
		"Loan Repayment": ["repay_from_salary", "payroll_payable_account"],
	}

	for doc, fields in custom_fields.items():
		filters = {"dt": doc, "fieldname": ["in", fields]}
		records = dontmanage.get_all("Custom Field", filters=filters, pluck="name")
		for record in records:
			dontmanage.delete_doc("Custom Field", record, ignore_missing=True, force=True)
