import dontmanage


def execute():
	dontmanage.reload_doc("stock", "doctype", "quality_inspection_parameter")

	# get all distinct parameters from QI readigs table
	reading_params = dontmanage.db.get_all(
		"Quality Inspection Reading", fields=["distinct specification"]
	)
	reading_params = [d.specification for d in reading_params]

	# get all distinct parameters from QI Template as some may be unused in QI
	template_params = dontmanage.db.get_all(
		"Item Quality Inspection Parameter", fields=["distinct specification"]
	)
	template_params = [d.specification for d in template_params]

	params = list(set(reading_params + template_params))

	for parameter in params:
		if not dontmanage.db.exists("Quality Inspection Parameter", parameter):
			dontmanage.get_doc(
				{"doctype": "Quality Inspection Parameter", "parameter": parameter, "description": parameter}
			).insert(ignore_permissions=True)
