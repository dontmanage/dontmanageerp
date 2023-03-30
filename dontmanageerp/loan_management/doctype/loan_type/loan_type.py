# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class LoanType(Document):
	def validate(self):
		self.validate_accounts()

	def validate_accounts(self):
		for fieldname in [
			"payment_account",
			"loan_account",
			"interest_income_account",
			"penalty_income_account",
		]:
			company = dontmanage.get_value("Account", self.get(fieldname), "company")

			if company and company != self.company:
				dontmanage.throw(
					_("Account {0} does not belong to company {1}").format(
						dontmanage.bold(self.get(fieldname)), dontmanage.bold(self.company)
					)
				)

		if self.get("loan_account") == self.get("payment_account"):
			dontmanage.throw(_("Loan Account and Payment Account cannot be same"))
