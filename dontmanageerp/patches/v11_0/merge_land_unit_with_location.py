# Copyright (c) 2018, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	# Rename and reload the Land Unit and Linked Land Unit doctypes
	if dontmanage.db.table_exists("Land Unit") and not dontmanage.db.table_exists("Location"):
		dontmanage.rename_doc("DocType", "Land Unit", "Location", force=True)

	dontmanage.reload_doc("assets", "doctype", "location")

	if dontmanage.db.table_exists("Linked Land Unit") and not dontmanage.db.table_exists("Linked Location"):
		dontmanage.rename_doc("DocType", "Linked Land Unit", "Linked Location", force=True)

	dontmanage.reload_doc("assets", "doctype", "linked_location")

	if not dontmanage.db.table_exists("Crop Cycle"):
		dontmanage.reload_doc("agriculture", "doctype", "crop_cycle")

	# Rename the fields in related doctypes
	if "linked_land_unit" in dontmanage.db.get_table_columns("Crop Cycle"):
		rename_field("Crop Cycle", "linked_land_unit", "linked_location")

	if "land_unit" in dontmanage.db.get_table_columns("Linked Location"):
		rename_field("Linked Location", "land_unit", "location")

	if not dontmanage.db.exists("Location", "All Land Units"):
		dontmanage.get_doc(
			{"doctype": "Location", "is_group": True, "location_name": "All Land Units"}
		).insert(ignore_permissions=True)

	if dontmanage.db.table_exists("Land Unit"):
		land_units = dontmanage.get_all("Land Unit", fields=["*"], order_by="lft")

		for land_unit in land_units:
			if not dontmanage.db.exists("Location", land_unit.get("land_unit_name")):
				dontmanage.get_doc(
					{
						"doctype": "Location",
						"location_name": land_unit.get("land_unit_name"),
						"parent_location": land_unit.get("parent_land_unit") or "All Land Units",
						"is_container": land_unit.get("is_container"),
						"is_group": land_unit.get("is_group"),
						"latitude": land_unit.get("latitude"),
						"longitude": land_unit.get("longitude"),
						"area": land_unit.get("area"),
						"location": land_unit.get("location"),
						"lft": land_unit.get("lft"),
						"rgt": land_unit.get("rgt"),
					}
				).insert(ignore_permissions=True)

	# Delete the Land Unit and Linked Land Unit doctypes
	if dontmanage.db.table_exists("Land Unit"):
		dontmanage.delete_doc("DocType", "Land Unit", force=1)

	if dontmanage.db.table_exists("Linked Land Unit"):
		dontmanage.delete_doc("DocType", "Linked Land Unit", force=1)
