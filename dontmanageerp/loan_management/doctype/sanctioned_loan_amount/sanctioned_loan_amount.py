# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class SanctionedLoanAmount(Document):
	def validate(self):
		sanctioned_doc = dontmanage.db.exists(
			"Sanctioned Loan Amount", {"applicant": self.applicant, "company": self.company}
		)

		if sanctioned_doc and sanctioned_doc != self.name:
			dontmanage.throw(
				_("Sanctioned Loan Amount already exists for {0} against company {1}").format(
					dontmanage.bold(self.applicant), dontmanage.bold(self.company)
				)
			)
