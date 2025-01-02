# Copyright (c) 2015, DontManage and Contributors and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class Operation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.manufacturing.doctype.sub_operation.sub_operation import SubOperation

		batch_size: DF.Int
		create_job_card_based_on_batch_size: DF.Check
		description: DF.Text | None
		is_corrective_operation: DF.Check
		quality_inspection_template: DF.Link | None
		sub_operations: DF.Table[SubOperation]
		total_operation_time: DF.Float
		workstation: DF.Link | None
	# end: auto-generated types

	def validate(self):
		if not self.description:
			self.description = self.name

		self.duplicate_sub_operation()
		self.set_total_time()

	def duplicate_sub_operation(self):
		operation_list = []
		for row in self.sub_operations:
			if row.operation in operation_list:
				dontmanage.throw(
					_("The operation {0} can not add multiple times").format(dontmanage.bold(row.operation))
				)

			if self.name == row.operation:
				dontmanage.throw(
					_("The operation {0} can not be the sub operation").format(dontmanage.bold(row.operation))
				)

			operation_list.append(row.operation)

	def set_total_time(self):
		self.total_operation_time = 0.0

		for row in self.sub_operations:
			self.total_operation_time += row.time_in_mins
