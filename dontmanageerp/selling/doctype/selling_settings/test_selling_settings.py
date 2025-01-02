# Copyright (c) 2019, DontManage and Contributors
# See license.txt

import unittest

import dontmanage


class TestSellingSettings(unittest.TestCase):
	def test_defaults_populated(self):
		# Setup default values are not populated on migrate, this test checks
		# if setup was completed correctly
		default = dontmanage.db.get_single_value("Selling Settings", "maintain_same_rate_action")
		self.assertEqual("Stop", default)
