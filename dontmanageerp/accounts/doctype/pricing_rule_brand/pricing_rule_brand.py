# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class PricingRuleBrand(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		brand: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		uom: DF.Link | None
	# end: auto-generated types

	pass