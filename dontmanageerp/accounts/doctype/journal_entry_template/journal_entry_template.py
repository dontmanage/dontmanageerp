# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class JournalEntryTemplate(Document):
	pass


@dontmanage.whitelist()
def get_naming_series():
	return dontmanage.get_meta("Journal Entry").get_field("naming_series").options
