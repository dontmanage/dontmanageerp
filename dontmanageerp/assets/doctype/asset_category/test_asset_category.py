# Copyright (c) 2015, DontManage and Contributors
# See license.txt

import unittest

import dontmanage


class TestAssetCategory(unittest.TestCase):
	def test_mandatory_fields(self):
		asset_category = dontmanage.new_doc("Asset Category")
		asset_category.asset_category_name = "Computers"

		self.assertRaises(dontmanage.MandatoryError, asset_category.insert)

		asset_category.total_number_of_depreciations = 3
		asset_category.frequency_of_depreciation = 3
		asset_category.append(
			"accounts",
			{
				"company_name": "_Test Company",
				"fixed_asset_account": "_Test Fixed Asset - _TC",
				"accumulated_depreciation_account": "_Test Accumulated Depreciations - _TC",
				"depreciation_expense_account": "_Test Depreciations - _TC",
			},
		)

		try:
			asset_category.insert(ignore_if_duplicate=True)
		except dontmanage.DuplicateEntryError:
			pass

	def test_cwip_accounting(self):
		company_cwip_acc = dontmanage.db.get_value(
			"Company", "_Test Company", "capital_work_in_progress_account"
		)
		dontmanage.db.set_value("Company", "_Test Company", "capital_work_in_progress_account", "")

		asset_category = dontmanage.new_doc("Asset Category")
		asset_category.asset_category_name = "Computers"
		asset_category.enable_cwip_accounting = 1

		asset_category.total_number_of_depreciations = 3
		asset_category.frequency_of_depreciation = 3
		asset_category.append(
			"accounts",
			{
				"company_name": "_Test Company",
				"fixed_asset_account": "_Test Fixed Asset - _TC",
				"accumulated_depreciation_account": "_Test Accumulated Depreciations - _TC",
				"depreciation_expense_account": "_Test Depreciations - _TC",
			},
		)

		self.assertRaises(dontmanage.ValidationError, asset_category.insert)
