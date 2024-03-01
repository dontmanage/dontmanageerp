# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class CostCenterAllocationPercentage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		cost_center: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Percent
	# end: auto-generated types

	pass
