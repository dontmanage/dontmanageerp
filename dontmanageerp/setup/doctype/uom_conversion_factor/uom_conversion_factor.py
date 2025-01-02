# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class UOMConversionFactor(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		category: DF.Link
		from_uom: DF.Link
		to_uom: DF.Link
		value: DF.Float
	# end: auto-generated types

	pass
