# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


# import dontmanage
from dontmanage.model.document import Document


class ServiceDay(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		end_time: DF.Time
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		start_time: DF.Time
		workday: DF.Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	# end: auto-generated types

	pass
