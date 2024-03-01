# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


# import dontmanage
from dontmanage.model.document import Document


class ProductionPlanSubAssemblyItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		actual_qty: DF.Float
		bom_level: DF.Int
		bom_no: DF.Link | None
		description: DF.SmallText | None
		fg_warehouse: DF.Link | None
		indent: DF.Int
		item_name: DF.Data | None
		parent: DF.Data
		parent_item_code: DF.Link | None
		parentfield: DF.Data
		parenttype: DF.Data
		production_item: DF.Link | None
		production_plan_item: DF.Data | None
		projected_qty: DF.Float
		purchase_order: DF.Link | None
		qty: DF.Float
		received_qty: DF.Float
		schedule_date: DF.Datetime | None
		stock_uom: DF.Link | None
		supplier: DF.Link | None
		type_of_manufacturing: DF.Literal["In House", "Subcontract", "Material Request"]
		uom: DF.Link | None
		wo_produced_qty: DF.Float
	# end: auto-generated types

	pass