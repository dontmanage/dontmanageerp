# Copyright (c) 2015, DontManage and Contributors and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class ProductBundleItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		description: DF.TextEditor | None
		item_code: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		rate: DF.Float
		uom: DF.Link | None
	# end: auto-generated types

	pass
