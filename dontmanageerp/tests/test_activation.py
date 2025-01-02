from dontmanage.tests.utils import DontManageTestCase

from dontmanageerp.utilities.activation import get_level


class TestActivation(DontManageTestCase):
	def test_activation(self):
		levels = get_level()
		self.assertTrue(levels)
