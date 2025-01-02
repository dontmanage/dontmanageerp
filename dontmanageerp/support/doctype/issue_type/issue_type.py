# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class IssueType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		description: DF.SmallText | None
	# end: auto-generated types

	pass
