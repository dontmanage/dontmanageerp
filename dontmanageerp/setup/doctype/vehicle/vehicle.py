# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import getdate


class Vehicle(Document):
	def validate(self):
		if getdate(self.start_date) > getdate(self.end_date):
			dontmanage.throw(_("Insurance Start date should be less than Insurance End date"))
		if getdate(self.carbon_check_date) > getdate():
			dontmanage.throw(_("Last carbon check date cannot be a future date"))
