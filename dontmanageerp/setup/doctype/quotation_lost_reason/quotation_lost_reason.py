# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


from dontmanage.model.document import Document


class QuotationLostReason(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		order_lost_reason: DF.Data
	# end: auto-generated types

	pass
