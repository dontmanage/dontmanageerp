# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document


class AssetShiftFactor(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		default: DF.Check
		shift_factor: DF.Float
		shift_name: DF.Data
	# end: auto-generated types

	def validate(self):
		self.validate_default()

	def validate_default(self):
		if self.default:
			existing_default_shift_factor = dontmanage.db.get_value(
				"Asset Shift Factor", {"default": 1}, "name"
			)

			if existing_default_shift_factor:
				dontmanage.throw(
					_("Asset Shift Factor {0} is set as default currently. Please change it first.").format(
						dontmanage.bold(existing_default_shift_factor)
					)
				)