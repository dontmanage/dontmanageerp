# Copyright (c) 2015, DontManage and Contributors
# MIT License. See license.txt


import unittest

import dontmanage
from dontmanage.desk import notifications


class TestNotifications(unittest.TestCase):
	def test_get_notifications_for_targets(self):
		"""
		Test notification config entries for targets as percentages
		"""

		company = dontmanage.get_all("Company")[0]
		dontmanage.db.set_value("Company", company.name, "monthly_sales_target", 10000)
		dontmanage.db.set_value("Company", company.name, "total_monthly_sales", 1000)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 10)

		dontmanage.db.set_value("Company", company.name, "monthly_sales_target", 2000)
		dontmanage.db.set_value("Company", company.name, "total_monthly_sales", 0)

		config = notifications.get_notification_config()
		doc_target_percents = notifications.get_notifications_for_targets(config, {})

		self.assertEqual(doc_target_percents["Company"][company.name], 0)
