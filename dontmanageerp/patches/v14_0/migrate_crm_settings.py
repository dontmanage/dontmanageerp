import dontmanage


def execute():
	settings = dontmanage.db.get_value(
		"Selling Settings",
		"Selling Settings",
		["campaign_naming_by", "close_opportunity_after_days", "default_valid_till"],
		as_dict=True,
	)

	dontmanage.reload_doc("crm", "doctype", "crm_settings")
	if settings:
		dontmanage.db.set_single_value(
			"CRM Settings",
			{
				"campaign_naming_by": settings.campaign_naming_by,
				"close_opportunity_after_days": settings.close_opportunity_after_days,
				"default_valid_till": settings.default_valid_till,
			},
		)
