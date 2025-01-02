# Copyright (c) 2022, DontManage and Contributors
# See license.txt

import dontmanage
from dontmanage.tests.utils import DontManageTestCase

from dontmanageerp.accounts.report.bank_reconciliation_statement.bank_reconciliation_statement import (
	execute,
)
from dontmanageerp.tests.utils import if_lending_app_installed


class TestBankReconciliationStatement(DontManageTestCase):
	def setUp(self):
		for dt in [
			"Journal Entry",
			"Journal Entry Account",
			"Payment Entry",
		]:
			dontmanage.db.delete(dt)
		clear_loan_transactions()

	@if_lending_app_installed
	def test_loan_entries_in_bank_reco_statement(self):
		from lending.loan_management.doctype.loan.test_loan import create_loan_accounts

		from dontmanageerp.accounts.doctype.bank_transaction.test_bank_transaction import (
			create_loan_and_repayment,
		)

		create_loan_accounts()

		repayment_entry = create_loan_and_repayment()

		filters = dontmanage._dict(
			{
				"company": "Test Company",
				"account": "Payment Account - _TC",
				"report_date": "2018-10-30",
			}
		)
		result = execute(filters)

		self.assertEqual(result[1][0].payment_entry, repayment_entry.name)


@if_lending_app_installed
def clear_loan_transactions():
	for dt in [
		"Loan Disbursement",
		"Loan Repayment",
	]:
		dontmanage.db.delete(dt)
