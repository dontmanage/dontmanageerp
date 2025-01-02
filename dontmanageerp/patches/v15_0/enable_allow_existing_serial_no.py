import dontmanage


def execute():
	if dontmanage.get_all("Company", filters={"country": "India"}, limit=1):
		dontmanage.db.set_single_value("Stock Settings", "allow_existing_serial_no", 1)
