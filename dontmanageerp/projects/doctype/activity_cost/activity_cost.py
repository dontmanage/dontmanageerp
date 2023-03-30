# Copyright (c) 2015, DontManage and Contributors and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class DuplicationError(dontmanage.ValidationError):
	pass


class ActivityCost(Document):
	def validate(self):
		self.set_title()
		self.check_unique()

	def set_title(self):
		if self.employee:
			if not self.employee_name:
				self.employee_name = dontmanage.db.get_value("Employee", self.employee, "employee_name")
			self.title = _("{0} for {1}").format(self.employee_name, self.activity_type)
		else:
			self.title = self.activity_type

	def check_unique(self):
		if self.employee:
			if dontmanage.db.sql(
				"""select name from `tabActivity Cost` where employee_name= %s and activity_type= %s and name != %s""",
				(self.employee_name, self.activity_type, self.name),
			):
				dontmanage.throw(
					_("Activity Cost exists for Employee {0} against Activity Type - {1}").format(
						self.employee, self.activity_type
					),
					DuplicationError,
				)
		else:
			if dontmanage.db.sql(
				"""select name from `tabActivity Cost` where ifnull(employee, '')='' and activity_type= %s and name != %s""",
				(self.activity_type, self.name),
			):
				dontmanage.throw(
					_("Default Activity Cost exists for Activity Type - {0}").format(self.activity_type),
					DuplicationError,
				)
