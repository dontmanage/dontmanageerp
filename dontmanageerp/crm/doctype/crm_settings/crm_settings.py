# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class CRMSettings(Document):
	def validate(self):
		dontmanage.db.set_default("campaign_naming_by", self.get("campaign_naming_by", ""))
