# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


from dontmanage.contacts.address_and_contact import load_address_and_contact
from dontmanage.model.document import Document


class Manufacturer(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
