import dontmanage


def execute():
	for stock_entry_type in [
		"Material Issue",
		"Material Receipt",
		"Material Transfer",
		"Material Transfer for Manufacture",
		"Material Consumption for Manufacture",
		"Manufacture",
		"Repack",
		"Send to Subcontractor",
		"Disassemble",
	]:
		if dontmanage.db.exists("Stock Entry Type", stock_entry_type):
			dontmanage.db.set_value("Stock Entry Type", stock_entry_type, "is_standard", 1)
