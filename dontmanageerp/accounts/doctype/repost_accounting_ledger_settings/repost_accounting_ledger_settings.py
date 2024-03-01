# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class RepostAccountingLedgerSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.repost_allowed_types.repost_allowed_types import RepostAllowedTypes

		allowed_types: DF.Table[RepostAllowedTypes]
	# end: auto-generated types

	pass
