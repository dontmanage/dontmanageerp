# Copyright (c) 2018, DontManage Technologies and contributors
# For license information, please see license.txt


from urllib.parse import urlencode

import dontmanage
import gocardless_pro
from dontmanage import _
from dontmanage.integrations.utils import create_request_log
from dontmanage.model.document import Document
from dontmanage.utils import call_hook_method, cint, flt, get_url

from dontmanageerp.utilities import payment_app_import_guard


class GoCardlessSettings(Document):
	supported_currencies = ["EUR", "DKK", "GBP", "SEK", "AUD", "NZD", "CAD", "USD"]

	def validate(self):
		self.initialize_client()

	def initialize_client(self):
		self.environment = self.get_environment()
		try:
			self.client = gocardless_pro.Client(
				access_token=self.access_token, environment=self.environment
			)
			return self.client
		except Exception as e:
			dontmanage.throw(e)

	def on_update(self):
		with payment_app_import_guard():
			from payments.utils import create_payment_gateway

		create_payment_gateway(
			"GoCardless-" + self.gateway_name, settings="GoCardLess Settings", controller=self.gateway_name
		)
		call_hook_method("payment_gateway_enabled", gateway="GoCardless-" + self.gateway_name)

	def on_payment_request_submission(self, data):
		if data.reference_doctype != "Fees":
			customer_data = dontmanage.db.get_value(
				data.reference_doctype, data.reference_name, ["company", "customer_name"], as_dict=1
			)

		data = {
			"amount": flt(data.grand_total, data.precision("grand_total")),
			"title": customer_data.company.encode("utf-8"),
			"description": data.subject.encode("utf-8"),
			"reference_doctype": data.doctype,
			"reference_docname": data.name,
			"payer_email": data.email_to or dontmanage.session.user,
			"payer_name": customer_data.customer_name,
			"order_id": data.name,
			"currency": data.currency,
		}

		valid_mandate = self.check_mandate_validity(data)
		if valid_mandate is not None:
			data.update(valid_mandate)

			self.create_payment_request(data)
			return False
		else:
			return True

	def check_mandate_validity(self, data):

		if dontmanage.db.exists("GoCardless Mandate", dict(customer=data.get("payer_name"), disabled=0)):
			registered_mandate = dontmanage.db.get_value(
				"GoCardless Mandate", dict(customer=data.get("payer_name"), disabled=0), "mandate"
			)
			self.initialize_client()
			mandate = self.client.mandates.get(registered_mandate)

			if (
				mandate.status == "pending_customer_approval"
				or mandate.status == "pending_submission"
				or mandate.status == "submitted"
				or mandate.status == "active"
			):
				return {"mandate": registered_mandate}
			else:
				return None
		else:
			return None

	def get_environment(self):
		if self.use_sandbox:
			return "sandbox"
		else:
			return "live"

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			dontmanage.throw(
				_(
					"Please select another payment method. Go Cardless does not support transactions in currency '{0}'"
				).format(currency)
			)

	def get_payment_url(self, **kwargs):
		return get_url("./integrations/gocardless_checkout?{0}".format(urlencode(kwargs)))

	def create_payment_request(self, data):
		self.data = dontmanage._dict(data)

		try:
			self.integration_request = create_request_log(self.data, "Host", "GoCardless")
			return self.create_charge_on_gocardless()

		except Exception:
			dontmanage.log_error("Gocardless payment reqeust failed")
			return {
				"redirect_to": dontmanage.redirect_to_message(
					_("Server Error"),
					_(
						"There seems to be an issue with the server's GoCardless configuration. Don't worry, in case of failure, the amount will get refunded to your account."
					),
				),
				"status": 401,
			}

	def create_charge_on_gocardless(self):
		redirect_to = self.data.get("redirect_to") or None
		redirect_message = self.data.get("redirect_message") or None

		reference_doc = dontmanage.get_doc(
			self.data.get("reference_doctype"), self.data.get("reference_docname")
		)
		self.initialize_client()

		try:
			payment = self.client.payments.create(
				params={
					"amount": cint(reference_doc.grand_total * 100),
					"currency": reference_doc.currency,
					"links": {"mandate": self.data.get("mandate")},
					"metadata": {
						"reference_doctype": reference_doc.doctype,
						"reference_document": reference_doc.name,
					},
				},
				headers={
					"Idempotency-Key": self.data.get("reference_docname"),
				},
			)

			if (
				payment.status == "pending_submission"
				or payment.status == "pending_customer_approval"
				or payment.status == "submitted"
			):
				self.integration_request.db_set("status", "Authorized", update_modified=False)
				self.flags.status_changed_to = "Completed"
				self.integration_request.db_set("output", payment.status, update_modified=False)

			elif payment.status == "confirmed" or payment.status == "paid_out":
				self.integration_request.db_set("status", "Completed", update_modified=False)
				self.flags.status_changed_to = "Completed"
				self.integration_request.db_set("output", payment.status, update_modified=False)

			elif (
				payment.status == "cancelled"
				or payment.status == "customer_approval_denied"
				or payment.status == "charged_back"
			):
				self.integration_request.db_set("status", "Cancelled", update_modified=False)
				dontmanage.log_error("Gocardless payment cancelled")
				self.integration_request.db_set("error", payment.status, update_modified=False)
			else:
				self.integration_request.db_set("status", "Failed", update_modified=False)
				dontmanage.log_error("Gocardless payment failed")
				self.integration_request.db_set("error", payment.status, update_modified=False)

		except Exception as e:
			dontmanage.log_error("GoCardless Payment Error")

		if self.flags.status_changed_to == "Completed":
			status = "Completed"
			if "reference_doctype" in self.data and "reference_docname" in self.data:
				custom_redirect_to = None
				try:
					custom_redirect_to = dontmanage.get_doc(
						self.data.get("reference_doctype"), self.data.get("reference_docname")
					).run_method("on_payment_authorized", self.flags.status_changed_to)
				except Exception:
					dontmanage.log_error("Gocardless redirect failed")

				if custom_redirect_to:
					redirect_to = custom_redirect_to

			redirect_url = redirect_to
		else:
			status = "Error"
			redirect_url = "payment-failed"

			if redirect_message:
				redirect_url += "&" + urlencode({"redirect_message": redirect_message})

			redirect_url = get_url(redirect_url)

		return {"redirect_to": redirect_url, "status": status}


def get_gateway_controller(doc):
	payment_request = dontmanage.get_doc("Payment Request", doc)
	gateway_controller = dontmanage.db.get_value(
		"Payment Gateway", payment_request.payment_gateway, "gateway_controller"
	)
	return gateway_controller


def gocardless_initialization(doc):
	gateway_controller = get_gateway_controller(doc)
	settings = dontmanage.get_doc("GoCardless Settings", gateway_controller)
	client = settings.initialize_client()
	return client
