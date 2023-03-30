# Copyright (c) 2015, DontManage and Contributors
# See license.txt

import unittest

import dontmanage
from dontmanage.utils import random_string

# test_records = dontmanage.get_test_records('Vehicle')


class TestVehicle(unittest.TestCase):
	def test_make_vehicle(self):
		vehicle = dontmanage.get_doc(
			{
				"doctype": "Vehicle",
				"license_plate": random_string(10).upper(),
				"make": "Maruti",
				"model": "PCM",
				"last_odometer": 5000,
				"acquisition_date": dontmanage.utils.nowdate(),
				"location": "Mumbai",
				"chassis_no": "1234ABCD",
				"uom": "Litre",
				"vehicle_value": dontmanage.utils.flt(500000),
			}
		)
		vehicle.insert()
