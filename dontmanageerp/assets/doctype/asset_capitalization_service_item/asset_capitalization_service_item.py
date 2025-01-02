# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class AssetCapitalizationServiceItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		amount: DF.Currency
		cost_center: DF.Link | None
		expense_account: DF.Link
		item_code: DF.Link | None
		item_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		qty: DF.Float
		rate: DF.Currency
		uom: DF.Link | None
	# end: auto-generated types

	pass
