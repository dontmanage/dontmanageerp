# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class QualityFeedback(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.quality_management.doctype.quality_feedback_parameter.quality_feedback_parameter import (
			QualityFeedbackParameter,
		)

		document_name: DF.DynamicLink
		document_type: DF.Literal["User", "Customer"]
		parameters: DF.Table[QualityFeedbackParameter]
		template: DF.Link
	# end: auto-generated types

	@dontmanage.whitelist()
	def set_parameters(self):
		if self.template and not getattr(self, "parameters", []):
			for d in dontmanage.get_doc("Quality Feedback Template", self.template).parameters:
				self.append("parameters", dict(parameter=d.parameter, rating=1))

	def validate(self):
		if not self.document_name:
			self.document_type = "User"
			self.document_name = dontmanage.session.user
		self.set_parameters()
