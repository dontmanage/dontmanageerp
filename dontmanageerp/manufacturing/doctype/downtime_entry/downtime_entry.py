# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document
from dontmanage.utils import time_diff_in_hours


class DowntimeEntry(Document):
	def validate(self):
		if self.from_time and self.to_time:
			self.downtime = time_diff_in_hours(self.to_time, self.from_time) * 60
