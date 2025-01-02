# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class DunningType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.dunning_letter_text.dunning_letter_text import DunningLetterText

		company: DF.Link
		cost_center: DF.Link | None
		dunning_fee: DF.Currency
		dunning_letter_text: DF.Table[DunningLetterText]
		dunning_type: DF.Data
		income_account: DF.Link | None
		is_default: DF.Check
		rate_of_interest: DF.Float
	# end: auto-generated types

	def autoname(self):
		company_abbr = dontmanage.get_value("Company", self.company, "abbr")
		self.name = f"{self.dunning_type} - {company_abbr}"
