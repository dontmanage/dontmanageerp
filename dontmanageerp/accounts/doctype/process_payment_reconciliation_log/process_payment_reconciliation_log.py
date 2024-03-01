# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

# import dontmanage
from dontmanage.model.document import Document


class ProcessPaymentReconciliationLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.process_payment_reconciliation_log_allocations.process_payment_reconciliation_log_allocations import (
			ProcessPaymentReconciliationLogAllocations,
		)

		allocated: DF.Check
		allocations: DF.Table[ProcessPaymentReconciliationLogAllocations]
		error_log: DF.LongText | None
		process_pr: DF.Link
		reconciled: DF.Check
		reconciled_entries: DF.Int
		status: DF.Literal[
			"Running", "Paused", "Reconciled", "Partially Reconciled", "Failed", "Cancelled"
		]
		total_allocations: DF.Int
	# end: auto-generated types

	pass
