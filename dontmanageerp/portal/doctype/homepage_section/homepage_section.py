# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document
from dontmanage.utils import cint


class HomepageSection(Document):
	@property
	def column_value(self):
		return cint(12 / cint(self.no_of_columns or 3))
