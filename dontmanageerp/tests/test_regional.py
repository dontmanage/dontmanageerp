import unittest

import dontmanage

import dontmanageerp


@dontmanageerp.allow_regional
def test_method():
	return "original"


class TestInit(unittest.TestCase):
	def test_regional_overrides(self):
		dontmanage.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")

		dontmanage.flags.country = "France"
		self.assertEqual(test_method(), "overridden")
