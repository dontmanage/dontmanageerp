# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class CashFlowMapping(Document):
	def validate(self):
		self.validate_checked_options()

	def validate_checked_options(self):
		checked_fields = [
			d for d in self.meta.fields if d.fieldtype == "Check" and self.get(d.fieldname) == 1
		]
		if len(checked_fields) > 1:
			dontmanage.throw(
				_("You can only select a maximum of one option from the list of check boxes."),
				title=_("Error"),
			)
