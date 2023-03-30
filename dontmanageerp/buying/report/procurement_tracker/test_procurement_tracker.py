# Copyright (c) 2013, DontManage and contributors
# For license information, please see license.txt


from datetime import datetime

import dontmanage
from dontmanage.tests.utils import DontManageTestCase

from dontmanageerp.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from dontmanageerp.buying.report.procurement_tracker.procurement_tracker import execute
from dontmanageerp.stock.doctype.material_request.material_request import make_purchase_order
from dontmanageerp.stock.doctype.material_request.test_material_request import make_material_request
from dontmanageerp.stock.doctype.warehouse.test_warehouse import create_warehouse


class TestProcurementTracker(DontManageTestCase):
	pass
