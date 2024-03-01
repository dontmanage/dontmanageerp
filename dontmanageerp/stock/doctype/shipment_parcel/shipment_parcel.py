# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


# import dontmanage
from dontmanage.model.document import Document


class ShipmentParcel(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		count: DF.Int
		height: DF.Int
		length: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		weight: DF.Float
		width: DF.Int
	# end: auto-generated types

	pass
