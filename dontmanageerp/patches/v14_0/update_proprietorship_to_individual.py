import dontmanage


def execute():
	for doctype in ["Customer", "Supplier"]:
		field = doctype.lower() + "_type"
		dontmanage.db.set_value(doctype, {field: "Proprietorship"}, field, "Individual")
