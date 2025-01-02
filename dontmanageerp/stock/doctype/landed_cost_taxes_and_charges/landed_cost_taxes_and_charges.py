# Copyright (c) 2015, DontManage and Contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class LandedCostTaxesandCharges(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		account_currency: DF.Link | None
		amount: DF.Currency
		base_amount: DF.Currency
		description: DF.SmallText
		exchange_rate: DF.Float
		expense_account: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
