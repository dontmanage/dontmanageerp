# -*- coding: utf-8 -*-
# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class Wishlist(Document):
	pass


@dontmanage.whitelist()
def add_to_wishlist(item_code):
	"""Insert Item into wishlist."""

	if dontmanage.db.exists("Wishlist Item", {"item_code": item_code, "parent": dontmanage.session.user}):
		return

	web_item_data = dontmanage.db.get_value(
		"Website Item",
		{"item_code": item_code},
		[
			"website_image",
			"website_warehouse",
			"name",
			"web_item_name",
			"item_name",
			"item_group",
			"route",
		],
		as_dict=1,
	)

	wished_item_dict = {
		"item_code": item_code,
		"item_name": web_item_data.get("item_name"),
		"item_group": web_item_data.get("item_group"),
		"website_item": web_item_data.get("name"),
		"web_item_name": web_item_data.get("web_item_name"),
		"image": web_item_data.get("website_image"),
		"warehouse": web_item_data.get("website_warehouse"),
		"route": web_item_data.get("route"),
	}

	if not dontmanage.db.exists("Wishlist", dontmanage.session.user):
		# initialise wishlist
		wishlist = dontmanage.get_doc({"doctype": "Wishlist"})
		wishlist.user = dontmanage.session.user
		wishlist.append("items", wished_item_dict)
		wishlist.save(ignore_permissions=True)
	else:
		wishlist = dontmanage.get_doc("Wishlist", dontmanage.session.user)
		item = wishlist.append("items", wished_item_dict)
		item.db_insert()

	if hasattr(dontmanage.local, "cookie_manager"):
		dontmanage.local.cookie_manager.set_cookie("wish_count", str(len(wishlist.items)))


@dontmanage.whitelist()
def remove_from_wishlist(item_code):
	if dontmanage.db.exists("Wishlist Item", {"item_code": item_code, "parent": dontmanage.session.user}):
		dontmanage.db.delete("Wishlist Item", {"item_code": item_code, "parent": dontmanage.session.user})
		dontmanage.db.commit()  # nosemgrep

		wishlist_items = dontmanage.db.get_values("Wishlist Item", filters={"parent": dontmanage.session.user})

		if hasattr(dontmanage.local, "cookie_manager"):
			dontmanage.local.cookie_manager.set_cookie("wish_count", str(len(wishlist_items)))
