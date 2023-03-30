# Copyright (c) 2020, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	dontmanage.reload_doc("setup", "doctype", "Email Digest")
	dontmanage.reload_doc("setup", "doctype", "Email Digest Recipient")
	email_digests = dontmanage.db.get_list("Email Digest", fields=["name", "recipient_list"])
	for email_digest in email_digests:
		if email_digest.recipient_list:
			for recipient in email_digest.recipient_list.split("\n"):
				doc = dontmanage.get_doc(
					{
						"doctype": "Email Digest Recipient",
						"parenttype": "Email Digest",
						"parentfield": "recipients",
						"parent": email_digest.name,
						"recipient": recipient,
					}
				)
				doc.insert()
