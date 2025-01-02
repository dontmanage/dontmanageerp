# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class SouthAfricaVATSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.south_africa_vat_account.south_africa_vat_account import (
			SouthAfricaVATAccount,
		)

		company: DF.Link
		vat_accounts: DF.Table[SouthAfricaVATAccount]
	# end: auto-generated types

	pass
