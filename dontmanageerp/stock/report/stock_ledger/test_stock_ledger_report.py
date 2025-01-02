# Copyright (c) 2022, DontManage and Contributors
# See license.txt

import dontmanage
from dontmanage.tests.utils import DontManageTestCase
from dontmanage.utils import add_days, today

from dontmanageerp.maintenance.doctype.maintenance_schedule.test_maintenance_schedule import (
	make_serial_item_with_serial,
)


class TestStockLedgerReeport(DontManageTestCase):
	def setUp(self) -> None:
		make_serial_item_with_serial("_Test Stock Report Serial Item")
		self.filters = dontmanage._dict(
			company="_Test Company",
			from_date=today(),
			to_date=add_days(today(), 30),
			item_code="_Test Stock Report Serial Item",
		)

	def tearDown(self) -> None:
		dontmanage.db.rollback()
