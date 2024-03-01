# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


from dontmanage.model.document import Document


class ItemWebsiteSpecification(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		description: DF.TextEditor | None
		label: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
