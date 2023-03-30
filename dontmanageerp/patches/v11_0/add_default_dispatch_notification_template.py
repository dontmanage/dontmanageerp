import os

import dontmanage
from dontmanage import _


def execute():
	dontmanage.reload_doc("email", "doctype", "email_template")
	dontmanage.reload_doc("stock", "doctype", "delivery_settings")

	if not dontmanage.db.exists("Email Template", _("Dispatch Notification")):
		base_path = dontmanage.get_app_path("dontmanageerp", "stock", "doctype")
		response = dontmanage.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		dontmanage.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": dontmanage.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = dontmanage.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
