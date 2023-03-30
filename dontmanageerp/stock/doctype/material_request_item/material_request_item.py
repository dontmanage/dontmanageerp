# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class MaterialRequestItem(Document):
	pass


def on_doctype_update():
	dontmanage.db.add_index("Material Request Item", ["item_code", "warehouse"])
