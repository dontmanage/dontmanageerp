# Copyright (c) 2022, DontManage and Contributors
# See license.txt

import dontmanage
from dontmanage.tests.utils import DontManageTestCase

from dontmanageerp.assets.doctype.asset.test_asset import create_asset, create_asset_data
from dontmanageerp.assets.doctype.asset_depreciation_schedule.asset_depreciation_schedule import (
	get_asset_depr_schedule_doc,
)


class TestAssetDepreciationSchedule(DontManageTestCase):
	def setUp(self):
		create_asset_data()

	def test_throw_error_if_another_asset_depr_schedule_exist(self):
		asset = create_asset(item_code="Macbook Pro", calculate_depreciation=1, submit=1)

		first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, "Active")
		self.assertEquals(first_asset_depr_schedule.status, "Active")

		second_asset_depr_schedule = dontmanage.get_doc(
			{"doctype": "Asset Depreciation Schedule", "asset": asset.name, "finance_book": None}
		)

		self.assertRaises(dontmanage.ValidationError, second_asset_depr_schedule.insert)
