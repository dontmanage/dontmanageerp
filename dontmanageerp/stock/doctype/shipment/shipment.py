# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.contacts.doctype.contact.contact import get_default_contact
from dontmanage.model.document import Document
from dontmanage.utils import flt, get_time

from dontmanageerp.accounts.party import get_party_shipping_address


class Shipment(Document):
	def validate(self):
		self.validate_weight()
		self.validate_pickup_time()
		self.set_value_of_goods()
		if self.docstatus == 0:
			self.status = "Draft"

	def on_submit(self):
		if not self.shipment_parcel:
			dontmanage.throw(_("Please enter Shipment Parcel information"))
		if self.value_of_goods == 0:
			dontmanage.throw(_("Value of goods cannot be 0"))
		self.db_set("status", "Submitted")

	def on_cancel(self):
		self.db_set("status", "Cancelled")

	def validate_weight(self):
		for parcel in self.shipment_parcel:
			if flt(parcel.weight) <= 0:
				dontmanage.throw(_("Parcel weight cannot be 0"))

	def validate_pickup_time(self):
		if self.pickup_from and self.pickup_to and get_time(self.pickup_to) < get_time(self.pickup_from):
			dontmanage.throw(_("Pickup To time should be greater than Pickup From time"))

	def set_value_of_goods(self):
		value_of_goods = 0
		for entry in self.get("shipment_delivery_note"):
			value_of_goods += flt(entry.get("grand_total"))
		self.value_of_goods = value_of_goods if value_of_goods else self.value_of_goods


@dontmanage.whitelist()
def get_address_name(ref_doctype, docname):
	# Return address name
	return get_party_shipping_address(ref_doctype, docname)


@dontmanage.whitelist()
def get_contact_name(ref_doctype, docname):
	# Return address name
	return get_default_contact(ref_doctype, docname)


@dontmanage.whitelist()
def get_company_contact(user):
	contact = dontmanage.db.get_value(
		"User",
		user,
		[
			"first_name",
			"last_name",
			"email",
			"phone",
			"mobile_no",
			"gender",
		],
		as_dict=1,
	)
	if not contact.phone:
		contact.phone = contact.mobile_no
	return contact
