import dontmanage
from dontmanage.tests.utils import DontManageTestCase

INDEXED_FIELDS = {
	"Bin": ["item_code"],
	"GL Entry": ["voucher_type", "against_voucher_type"],
	"Purchase Order Item": ["item_code"],
	"Stock Ledger Entry": ["warehouse"],
}


class TestPerformance(DontManageTestCase):
	def test_ensure_indexes(self):
		# These fields are not explicitly indexed BUT they are prefix in some
		# other composite index. If those are removed this test should be
		# updated accordingly.
		for doctype, fields in INDEXED_FIELDS.items():
			for field in fields:
				self.assertTrue(
					dontmanage.db.sql(
						f"""SHOW INDEX FROM `tab{doctype}`
						WHERE Column_name = "{field}" AND Seq_in_index = 1"""
					)
				)
