# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage

from dontmanageerp.setup.doctype.company.company import install_country_fixtures


def execute():
	dontmanage.reload_doc("regional", "report", "fichier_des_ecritures_comptables_[fec]")
	for d in dontmanage.get_all("Company", filters={"country": "France"}):
		install_country_fixtures(d.name)
