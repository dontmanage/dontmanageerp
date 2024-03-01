# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class BOMWebsiteOperation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		operation: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		thumbnail: DF.Data | None
		time_in_mins: DF.Float
		website_image: DF.Attach | None
		workstation: DF.Link | None
	# end: auto-generated types

	pass
