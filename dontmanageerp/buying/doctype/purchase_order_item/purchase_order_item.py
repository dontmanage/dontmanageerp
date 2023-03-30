# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.document import Document


class PurchaseOrderItem(Document):
	pass


def on_doctype_update():
	dontmanage.db.add_index("Purchase Order Item", ["item_code", "warehouse"])
