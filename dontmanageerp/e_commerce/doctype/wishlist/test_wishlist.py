# -*- coding: utf-8 -*-
# Copyright (c) 2021, DontManage and Contributors
# See license.txt
import unittest

import dontmanage
from dontmanage.core.doctype.user_permission.test_user_permission import create_user

from dontmanageerp.e_commerce.doctype.website_item.website_item import make_website_item
from dontmanageerp.e_commerce.doctype.wishlist.wishlist import add_to_wishlist, remove_from_wishlist
from dontmanageerp.stock.doctype.item.test_item import make_item


class TestWishlist(unittest.TestCase):
	def setUp(self):
		item = make_item("Test Phone Series X")
		if not dontmanage.db.exists("Website Item", {"item_code": "Test Phone Series X"}):
			make_website_item(item, save=True)

		item = make_item("Test Phone Series Y")
		if not dontmanage.db.exists("Website Item", {"item_code": "Test Phone Series Y"}):
			make_website_item(item, save=True)

	def tearDown(self):
		dontmanage.get_cached_doc("Website Item", {"item_code": "Test Phone Series X"}).delete()
		dontmanage.get_cached_doc("Website Item", {"item_code": "Test Phone Series Y"}).delete()
		dontmanage.get_cached_doc("Item", "Test Phone Series X").delete()
		dontmanage.get_cached_doc("Item", "Test Phone Series Y").delete()

	def test_add_remove_items_in_wishlist(self):
		"Check if items are added and removed from user's wishlist."
		# add first item
		add_to_wishlist("Test Phone Series X")

		# check if wishlist was created and item was added
		self.assertTrue(dontmanage.db.exists("Wishlist", {"user": dontmanage.session.user}))
		self.assertTrue(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": dontmanage.session.user}
			)
		)

		# add second item to wishlist
		add_to_wishlist("Test Phone Series Y")
		wishlist_length = dontmanage.db.get_value(
			"Wishlist Item", {"parent": dontmanage.session.user}, "count(*)"
		)
		self.assertEqual(wishlist_length, 2)

		remove_from_wishlist("Test Phone Series X")
		remove_from_wishlist("Test Phone Series Y")

		wishlist_length = dontmanage.db.get_value(
			"Wishlist Item", {"parent": dontmanage.session.user}, "count(*)"
		)
		self.assertIsNone(dontmanage.db.exists("Wishlist Item", {"parent": dontmanage.session.user}))
		self.assertEqual(wishlist_length, 0)

		# tear down
		dontmanage.get_doc("Wishlist", {"user": dontmanage.session.user}).delete()

	def test_add_remove_in_wishlist_multiple_users(self):
		"Check if items are added and removed from the correct user's wishlist."
		test_user = create_user("test_reviewer@example.com", "Customer")
		test_user_1 = create_user("test_reviewer_1@example.com", "Customer")

		# add to wishlist for first user
		dontmanage.set_user(test_user.name)
		add_to_wishlist("Test Phone Series X")

		# add to wishlist for second user
		dontmanage.set_user(test_user_1.name)
		add_to_wishlist("Test Phone Series X")

		# check wishlist and its content for users
		self.assertTrue(dontmanage.db.exists("Wishlist", {"user": test_user.name}))
		self.assertTrue(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		self.assertTrue(dontmanage.db.exists("Wishlist", {"user": test_user_1.name}))
		self.assertTrue(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user_1.name}
			)
		)

		# remove item for second user
		remove_from_wishlist("Test Phone Series X")

		# make sure item was removed for second user and not first
		self.assertFalse(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user_1.name}
			)
		)
		self.assertTrue(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		# remove item for first user
		dontmanage.set_user(test_user.name)
		remove_from_wishlist("Test Phone Series X")
		self.assertFalse(
			dontmanage.db.exists(
				"Wishlist Item", {"item_code": "Test Phone Series X", "parent": test_user.name}
			)
		)

		# tear down
		dontmanage.set_user("Administrator")
		dontmanage.get_doc("Wishlist", {"user": test_user.name}).delete()
		dontmanage.get_doc("Wishlist", {"user": test_user_1.name}).delete()
