# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class CustomsTariffNumber(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		description: DF.Data | None
		tariff_number: DF.Data
	# end: auto-generated types

	pass