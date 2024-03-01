# Copyright (c) 2019, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document
from dontmanage.utils import cint


class HomepageSection(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.portal.doctype.homepage_section_card.homepage_section_card import (
			HomepageSectionCard,
		)

		no_of_columns: DF.Literal["1", "2", "3", "4", "6"]
		section_based_on: DF.Literal["Cards", "Custom HTML"]
		section_cards: DF.Table[HomepageSectionCard]
		section_html: DF.Code | None
		section_order: DF.Int
	# end: auto-generated types

	@property
	def column_value(self):
		return cint(12 / cint(self.no_of_columns or 3))
