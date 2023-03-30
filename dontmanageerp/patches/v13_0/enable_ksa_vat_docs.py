import dontmanage

from dontmanageerp.regional.saudi_arabia.setup import add_permissions, add_print_formats


def execute():
	company = dontmanage.get_all("Company", filters={"country": "Saudi Arabia"})
	if not company:
		return

	add_print_formats()
	add_permissions()
