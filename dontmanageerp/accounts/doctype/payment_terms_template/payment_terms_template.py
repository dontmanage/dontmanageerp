# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import flt


class PaymentTermsTemplate(Document):
	def validate(self):
		self.validate_invoice_portion()
		self.check_duplicate_terms()

	def validate_invoice_portion(self):
		total_portion = 0
		for term in self.terms:
			total_portion += flt(term.get("invoice_portion", 0))

		if flt(total_portion, 2) != 100.00:
			dontmanage.msgprint(
				_("Combined invoice portion must equal 100%"), raise_exception=1, indicator="red"
			)

	def check_duplicate_terms(self):
		terms = []
		for term in self.terms:
			term_info = (term.payment_term, term.credit_days, term.credit_months, term.due_date_based_on)
			if term_info in terms:
				dontmanage.msgprint(
					_("The Payment Term at row {0} is possibly a duplicate.").format(term.idx),
					raise_exception=1,
					indicator="red",
				)
			else:
				terms.append(term_info)
