import dontmanage


def execute():
	dontmanage.reload_doctype("Employee")
	dontmanage.db.sql("update tabEmployee set first_name = employee_name")

	# update holiday list
	dontmanage.reload_doctype("Holiday List")
	for holiday_list in dontmanage.get_all("Holiday List"):
		holiday_list = dontmanage.get_doc("Holiday List", holiday_list.name)
		holiday_list.db_set("total_holidays", len(holiday_list.holidays), update_modified=False)
