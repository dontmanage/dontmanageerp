# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.regional.italy.setup import add_permissions


def execute():
	countries = dontmanage.get_all("Company", fields="country")
	countries = [country["country"] for country in countries]
	if "Italy" in countries:
		add_permissions()
