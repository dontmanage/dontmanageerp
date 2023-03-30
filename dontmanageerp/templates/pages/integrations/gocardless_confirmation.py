# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage
from dontmanage import _

from dontmanageerp.dontmanageerp_integrations.doctype.gocardless_settings.gocardless_settings import (
	get_gateway_controller,
	gocardless_initialization,
)

no_cache = 1

expected_keys = ("redirect_flow_id", "reference_doctype", "reference_docname")


def get_context(context):
	context.no_cache = 1

	# all these keys exist in form_dict
	if not (set(expected_keys) - set(dontmanage.form_dict.keys())):
		for key in expected_keys:
			context[key] = dontmanage.form_dict[key]

	else:
		dontmanage.redirect_to_message(
			_("Some information is missing"),
			_("Looks like someone sent you to an incomplete URL. Please ask them to look into it."),
		)
		dontmanage.local.flags.redirect_location = dontmanage.local.response.location
		raise dontmanage.Redirect


@dontmanage.whitelist(allow_guest=True)
def confirm_payment(redirect_flow_id, reference_doctype, reference_docname):

	client = gocardless_initialization(reference_docname)

	try:
		redirect_flow = client.redirect_flows.complete(
			redirect_flow_id, params={"session_token": dontmanage.session.user}
		)

		confirmation_url = redirect_flow.confirmation_url
		gocardless_success_page = dontmanage.get_hooks("gocardless_success_page")
		if gocardless_success_page:
			confirmation_url = dontmanage.get_attr(gocardless_success_page[-1])(
				reference_doctype, reference_docname
			)

		data = {
			"mandate": redirect_flow.links.mandate,
			"customer": redirect_flow.links.customer,
			"redirect_to": confirmation_url,
			"redirect_message": "Mandate successfully created",
			"reference_doctype": reference_doctype,
			"reference_docname": reference_docname,
		}

		try:
			create_mandate(data)
		except Exception as e:
			dontmanage.log_error("GoCardless Mandate Registration Error")

		gateway_controller = get_gateway_controller(reference_docname)
		dontmanage.get_doc("GoCardless Settings", gateway_controller).create_payment_request(data)

		return {"redirect_to": confirmation_url}

	except Exception as e:
		dontmanage.log_error("GoCardless Payment Error")
		return {"redirect_to": "/integrations/payment-failed"}


def create_mandate(data):
	data = dontmanage._dict(data)
	dontmanage.logger().debug(data)

	mandate = data.get("mandate")

	if dontmanage.db.exists("GoCardless Mandate", mandate):
		return

	else:
		reference_doc = dontmanage.db.get_value(
			data.get("reference_doctype"),
			data.get("reference_docname"),
			["reference_doctype", "reference_name"],
			as_dict=1,
		)
		dontmanageerp_customer = dontmanage.db.get_value(
			reference_doc.reference_doctype, reference_doc.reference_name, ["customer_name"], as_dict=1
		)

		try:
			dontmanage.get_doc(
				{
					"doctype": "GoCardless Mandate",
					"mandate": mandate,
					"customer": dontmanageerp_customer.customer_name,
					"gocardless_customer": data.get("customer"),
				}
			).insert(ignore_permissions=True)

		except Exception:
			dontmanage.log_error("Gocardless: Unable to create mandate")
