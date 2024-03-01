# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class TelephonyCallType(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		amended_from: DF.Link | None
		call_type: DF.Data
	# end: auto-generated types

	pass
