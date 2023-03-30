# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


import dontmanage
import requests
from dontmanage import _
from dontmanage.model.document import Document


class ExotelSettings(Document):
	def validate(self):
		self.verify_credentials()

	def verify_credentials(self):
		if self.enabled:
			response = requests.get(
				"https://api.exotel.com/v1/Accounts/{sid}".format(sid=self.account_sid),
				auth=(self.api_key, self.api_token),
			)
			if response.status_code != 200:
				dontmanage.throw(_("Invalid credentials"))
