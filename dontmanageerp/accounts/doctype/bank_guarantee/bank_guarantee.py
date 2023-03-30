# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class BankGuarantee(Document):
	def validate(self):
		if not (self.customer or self.supplier):
			dontmanage.throw(_("Select the customer or supplier."))

	def on_submit(self):
		if not self.bank_guarantee_number:
			dontmanage.throw(_("Enter the Bank Guarantee Number before submittting."))
		if not self.name_of_beneficiary:
			dontmanage.throw(_("Enter the name of the Beneficiary before submittting."))
		if not self.bank:
			dontmanage.throw(_("Enter the name of the bank or lending institution before submittting."))


@dontmanage.whitelist()
def get_voucher_details(bank_guarantee_type: str, reference_name: str):
	if not isinstance(reference_name, str):
		raise TypeError("reference_name must be a string")

	fields_to_fetch = ["grand_total"]

	if bank_guarantee_type == "Receiving":
		doctype = "Sales Order"
		fields_to_fetch.append("customer")
		fields_to_fetch.append("project")
	else:
		doctype = "Purchase Order"
		fields_to_fetch.append("supplier")

	return dontmanage.db.get_value(doctype, reference_name, fields_to_fetch, as_dict=True)
