# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


from dontmanage.model.document import Document


class PurchaseInvoiceAdvance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		advance_amount: DF.Currency
		allocated_amount: DF.Currency
		exchange_gain_loss: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		ref_exchange_rate: DF.Float
		reference_name: DF.DynamicLink | None
		reference_row: DF.Data | None
		reference_type: DF.Link | None
		remarks: DF.Text | None
	# end: auto-generated types

	pass
