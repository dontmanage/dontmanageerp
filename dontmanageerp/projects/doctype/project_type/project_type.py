# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class ProjectType(Document):
	def on_trash(self):
		if self.name == "External":
			dontmanage.throw(_("You cannot delete Project Type 'External'"))
