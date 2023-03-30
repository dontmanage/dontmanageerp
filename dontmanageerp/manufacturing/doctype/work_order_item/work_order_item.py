# Copyright (c) 2015, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class WorkOrderItem(Document):
	pass


def on_doctype_update():
	dontmanage.db.add_index("Work Order Item", ["item_code", "source_warehouse"])
