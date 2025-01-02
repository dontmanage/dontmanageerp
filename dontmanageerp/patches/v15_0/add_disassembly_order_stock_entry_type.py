import dontmanage


def execute():
	if not dontmanage.db.exists("Stock Entry Type", "Disassemble"):
		dontmanage.get_doc(
			{
				"doctype": "Stock Entry Type",
				"name": "Disassemble",
				"purpose": "Disassemble",
				"is_standard": 1,
			}
		).insert(ignore_permissions=True)
