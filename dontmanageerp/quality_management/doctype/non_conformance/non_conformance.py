# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


# import dontmanage
from dontmanage.model.document import Document


class NonConformance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		corrective_action: DF.TextEditor | None
		details: DF.TextEditor | None
		full_name: DF.Data | None
		preventive_action: DF.TextEditor | None
		procedure: DF.Link
		process_owner: DF.Data | None
		status: DF.Literal["Open", "Resolved", "Cancelled"]
		subject: DF.Data
	# end: auto-generated types

	pass
