import dontmanage


def execute():
	if dontmanage.db.exists("DocType", "Lost Reason Detail"):
		dontmanage.reload_doc("crm", "doctype", "opportunity_lost_reason")
		dontmanage.reload_doc("crm", "doctype", "opportunity_lost_reason_detail")
		dontmanage.reload_doc("setup", "doctype", "quotation_lost_reason_detail")

		dontmanage.db.sql(
			"""INSERT INTO `tabOpportunity Lost Reason Detail` SELECT * FROM `tabLost Reason Detail` WHERE `parenttype` = 'Opportunity'"""
		)

		dontmanage.db.sql(
			"""INSERT INTO `tabQuotation Lost Reason Detail` SELECT * FROM `tabLost Reason Detail` WHERE `parenttype` = 'Quotation'"""
		)

		dontmanage.db.sql(
			"""INSERT INTO `tabQuotation Lost Reason` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `_comments`, `_assign`, `_user_tags`, `_liked_by`, `order_lost_reason`)
            SELECT o.`name`, o.`creation`, o.`modified`, o.`modified_by`, o.`owner`, o.`docstatus`, o.`parent`, o.`parentfield`, o.`parenttype`, o.`idx`, o.`_comments`, o.`_assign`, o.`_user_tags`, o.`_liked_by`, o.`lost_reason`
            FROM `tabOpportunity Lost Reason` o LEFT JOIN `tabQuotation Lost Reason` q ON q.name = o.name WHERE q.name IS NULL"""
		)

		dontmanage.delete_doc("DocType", "Lost Reason Detail")
