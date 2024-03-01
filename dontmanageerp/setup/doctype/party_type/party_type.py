# Copyright (c) 2015, DontManage Technologies and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class PartyType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		account_type: DF.Literal["Payable", "Receivable"]
		party_type: DF.Link
	# end: auto-generated types

	pass


@dontmanage.whitelist()
@dontmanage.validate_and_sanitize_search_inputs
def get_party_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ""
	if filters and filters.get("account"):
		account_type = dontmanage.db.get_value("Account", filters.get("account"), "account_type")
		cond = "and account_type = '%s'" % account_type

	return dontmanage.db.sql(
		"""select name from `tabParty Type`
			where `{key}` LIKE %(txt)s {cond}
			order by name limit %(page_len)s offset %(start)s""".format(
			key=searchfield, cond=cond
		),
		{"txt": "%" + txt + "%", "start": start, "page_len": page_len},
	)
