# Copyright (c) 2021, DontManage and Contributors
# See license.txt

import unittest

import dontmanage

from dontmanageerp.stock.doctype.repost_item_valuation.repost_item_valuation import get_recipients


class TestStockRepostingSettings(unittest.TestCase):
	def test_notify_reposting_error_to_role(self):
		role = "Notify Reposting Role"

		if not dontmanage.db.exists("Role", role):
			dontmanage.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)

		user = "notify_reposting_error@test.com"
		if not dontmanage.db.exists("User", user):
			dontmanage.get_doc(
				{
					"doctype": "User",
					"email": user,
					"first_name": "Test",
					"language": "en",
					"time_zone": "Asia/Kolkata",
					"send_welcome_email": 0,
					"roles": [{"role": role}],
				}
			).insert(ignore_permissions=True)

		dontmanage.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", "")

		users = get_recipients()
		self.assertFalse(user in users)

		dontmanage.db.set_single_value("Stock Reposting Settings", "notify_reposting_error_to_role", role)

		users = get_recipients()
		self.assertTrue(user in users)
