import dontmanage


def execute():
	dontmanage.reload_doc("core", "doctype", "scheduled_job_type")
	if dontmanage.db.exists("Scheduled Job Type", "repost_item_valuation.repost_entries"):
		dontmanage.db.set_value("Scheduled Job Type", "repost_item_valuation.repost_entries", "stopped", 0)
