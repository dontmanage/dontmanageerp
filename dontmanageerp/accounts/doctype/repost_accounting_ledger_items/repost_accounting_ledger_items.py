# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class RepostAccountingLedgerItems(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		voucher_no: DF.DynamicLink | None
		voucher_type: DF.Link | None
	# end: auto-generated types

	pass
