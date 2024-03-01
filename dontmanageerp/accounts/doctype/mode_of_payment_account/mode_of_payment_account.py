# Copyright (c) 2015, DontManage and Contributors and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class ModeofPaymentAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		company: DF.Link | None
		default_account: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
