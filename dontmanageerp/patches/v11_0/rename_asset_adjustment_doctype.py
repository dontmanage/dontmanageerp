# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage


def execute():
	if dontmanage.db.table_exists("Asset Adjustment") and not dontmanage.db.table_exists(
		"Asset Value Adjustment"
	):
		dontmanage.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		dontmanage.reload_doc("assets", "doctype", "asset_value_adjustment")
