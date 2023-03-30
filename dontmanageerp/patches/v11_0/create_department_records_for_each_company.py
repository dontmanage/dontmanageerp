import dontmanage
from dontmanage import _
from dontmanage.utils.nestedset import rebuild_tree


def execute():
	dontmanage.local.lang = dontmanage.db.get_default("lang") or "en"

	for doctype in ["department", "leave_period", "staffing_plan", "job_opening"]:
		dontmanage.reload_doc("hr", "doctype", doctype)
	dontmanage.reload_doc("Payroll", "doctype", "payroll_entry")

	companies = dontmanage.db.get_all("Company", fields=["name", "abbr"])
	departments = dontmanage.db.get_all("Department")
	comp_dict = {}

	# create a blank list for each company
	for company in companies:
		comp_dict[company.name] = {}

	for department in departments:
		# skip root node
		if _(department.name) == _("All Departments"):
			continue

		# for each company, create a copy of the doc
		department_doc = dontmanage.get_doc("Department", department)
		for company in companies:
			copy_doc = dontmanage.copy_doc(department_doc)
			copy_doc.update({"company": company.name})
			try:
				copy_doc.insert()
			except dontmanage.DuplicateEntryError:
				pass
			# append list of new department for each company
			comp_dict[company.name][department.name] = copy_doc.name

	rebuild_tree("Department", "parent_department")
	doctypes = ["Asset", "Employee", "Payroll Entry", "Staffing Plan", "Job Opening"]

	for d in doctypes:
		update_records(d, comp_dict)

	update_instructors(comp_dict)

	dontmanage.local.lang = "en"


def update_records(doctype, comp_dict):
	when_then = []
	for company in comp_dict:
		records = comp_dict[company]

		for department in records:
			when_then.append(
				"""
				WHEN company = "%s" and department = "%s"
				THEN "%s"
			"""
				% (company, department, records[department])
			)

	if not when_then:
		return

	dontmanage.db.sql(
		"""
		update
			`tab%s`
		set
			department = CASE %s END
	"""
		% (doctype, " ".join(when_then))
	)


def update_instructors(comp_dict):
	when_then = []
	emp_details = dontmanage.get_all("Employee", fields=["name", "company"])

	for employee in emp_details:
		records = comp_dict[employee.company] if employee.company else []

		for department in records:
			when_then.append(
				"""
				WHEN employee = "%s" and department = "%s"
				THEN "%s"
			"""
				% (employee.name, department, records[department])
			)

	if not when_then:
		return

	dontmanage.db.sql(
		"""
		update
			`tabInstructor`
		set
			department = CASE %s END
	"""
		% (" ".join(when_then))
	)
