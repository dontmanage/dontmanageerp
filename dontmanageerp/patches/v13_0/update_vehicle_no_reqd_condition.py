import dontmanage


def execute():
	dontmanage.reload_doc("custom", "doctype", "custom_field", force=True)
	company = dontmanage.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if dontmanage.db.exists("Custom Field", {"fieldname": "vehicle_no"}):
		dontmanage.db.set_value("Custom Field", {"fieldname": "vehicle_no"}, "mandatory_depends_on", "")
