# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class ProjectType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		description: DF.Text | None
		project_type: DF.Data
	# end: auto-generated types

	def on_trash(self):
		if self.name == "External":
			dontmanage.throw(_("You cannot delete Project Type 'External'"))
