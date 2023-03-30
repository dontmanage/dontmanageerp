# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import flt


class WorkstationType(Document):
	def before_save(self):
		self.set_hour_rate()

	def set_hour_rate(self):
		self.hour_rate = (
			flt(self.hour_rate_labour)
			+ flt(self.hour_rate_electricity)
			+ flt(self.hour_rate_consumable)
			+ flt(self.hour_rate_rent)
		)


def get_workstations(workstation_type):
	workstations = dontmanage.get_all("Workstation", filters={"workstation_type": workstation_type})

	return [workstation.name for workstation in workstations]
