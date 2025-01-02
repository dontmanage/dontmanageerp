# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class AdvanceTax(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		account_head: DF.Link | None
		allocated_amount: DF.Currency
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference_detail: DF.Data | None
		reference_name: DF.DynamicLink | None
		reference_type: DF.Link | None
	# end: auto-generated types

	pass
