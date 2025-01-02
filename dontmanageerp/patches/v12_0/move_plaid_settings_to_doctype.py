# Copyright (c) 2017, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("dontmanageerp_integrations", "doctype", "plaid_settings")
	plaid_settings = dontmanage.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (dontmanage.conf.plaid_client_id and dontmanage.conf.plaid_env and dontmanage.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": dontmanage.conf.plaid_client_id,
					"plaid_env": dontmanage.conf.plaid_env,
					"plaid_secret": dontmanage.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
