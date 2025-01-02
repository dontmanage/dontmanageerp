# Copyright (c) 2024, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class TransactionDeletionRecordDetails(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		docfield_name: DF.Data | None
		doctype_name: DF.Link
		done: DF.Check
		no_of_docs: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types

	pass
