# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import flt


class CashierClosing(Document):
	def validate(self):
		self.validate_time()

	def before_save(self):
		self.get_outstanding()
		self.make_calculations()

	def get_outstanding(self):
		values = dontmanage.db.sql(
			"""
			select sum(outstanding_amount)
			from `tabSales Invoice`
			where posting_date=%s and posting_time>=%s and posting_time<=%s and owner=%s
		""",
			(self.date, self.from_time, self.time, self.user),
		)
		self.outstanding_amount = flt(values[0][0] if values else 0)

	def make_calculations(self):
		total = 0.00
		for i in self.payments:
			total += flt(i.amount)

		self.net_amount = (
			total + self.outstanding_amount + flt(self.expense) - flt(self.custody) + flt(self.returns)
		)

	def validate_time(self):
		if self.from_time >= self.time:
			dontmanage.throw(_("From Time Should Be Less Than To Time"))
