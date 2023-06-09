# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


@dontmanage.whitelist(allow_guest=True)
def send_message(subject="Website Query", message="", sender="", status="Open"):
	from dontmanage.www.contact import send_message as website_send_message

	lead = customer = None

	website_send_message(subject, message, sender)

	customer = dontmanage.db.sql(
		"""select distinct dl.link_name from `tabDynamic Link` dl
		left join `tabContact` c on dl.parent=c.name where dl.link_doctype='Customer'
		and c.email_id = %s""",
		sender,
	)

	if not customer:
		lead = dontmanage.db.get_value("Lead", dict(email_id=sender))
		if not lead:
			new_lead = dontmanage.get_doc(
				dict(doctype="Lead", email_id=sender, lead_name=sender.split("@")[0].title())
			).insert(ignore_permissions=True)

	opportunity = dontmanage.get_doc(
		dict(
			doctype="Opportunity",
			opportunity_from="Customer" if customer else "Lead",
			status="Open",
			title=subject,
			contact_email=sender,
		)
	)

	if customer:
		opportunity.party_name = customer[0][0]
	elif lead:
		opportunity.party_name = lead
	else:
		opportunity.party_name = new_lead.name

	opportunity.insert(ignore_permissions=True)

	comm = dontmanage.get_doc(
		{
			"doctype": "Communication",
			"subject": subject,
			"content": message,
			"sender": sender,
			"sent_or_received": "Received",
			"reference_doctype": "Opportunity",
			"reference_name": opportunity.name,
		}
	)
	comm.insert(ignore_permissions=True)

	return "okay"
