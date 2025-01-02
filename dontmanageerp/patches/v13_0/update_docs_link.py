# Copyright (c) 2023, DontManage and Contributors
# License: MIT. See LICENSE


import dontmanage


def execute():
	navbar_settings = dontmanage.get_single("Navbar Settings")
	for item in navbar_settings.help_dropdown:
		if item.is_standard and item.route == "https://dontmanageerp.com/docs/user/manual":
			item.route = "https://docs.dontmanageerp.com/docs/v14/user/manual/en/introduction"

	navbar_settings.save()
