import dontmanage

# Set department value based on employee value


def execute():

	doctypes_to_update = {
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if dontmanage.db.table_exists(doctype):
				dontmanage.reload_doc(module, "doctype", dontmanage.scrub(doctype))
				dontmanage.db.sql(
					"""
					update `tab%s` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
				"""
					% doctype
				)
