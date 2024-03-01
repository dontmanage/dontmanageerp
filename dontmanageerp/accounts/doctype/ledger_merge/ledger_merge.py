# Copyright (c) 2021, Wahni Green Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils.background_jobs import is_job_enqueued

from dontmanageerp.accounts.doctype.account.account import merge_account


class LedgerMerge(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.ledger_merge_accounts.ledger_merge_accounts import (
			LedgerMergeAccounts,
		)

		account: DF.Link
		account_name: DF.Data
		company: DF.Link
		is_group: DF.Check
		merge_accounts: DF.Table[LedgerMergeAccounts]
		root_type: DF.Literal["", "Asset", "Liability", "Income", "Expense", "Equity"]
		status: DF.Literal["Pending", "Success", "Partial Success", "Error"]
	# end: auto-generated types

	def start_merge(self):
		from dontmanage.utils.background_jobs import enqueue
		from dontmanage.utils.scheduler import is_scheduler_inactive

		if is_scheduler_inactive() and not dontmanage.flags.in_test:
			dontmanage.throw(_("Scheduler is inactive. Cannot merge accounts."), title=_("Scheduler Inactive"))

		job_id = f"ledger_merge::{self.name}"
		if not is_job_enqueued(job_id):
			enqueue(
				start_merge,
				queue="default",
				timeout=6000,
				event="ledger_merge",
				job_id=job_id,
				docname=self.name,
				now=dontmanage.conf.developer_mode or dontmanage.flags.in_test,
			)
			return True

		return False


@dontmanage.whitelist()
def form_start_merge(docname):
	return dontmanage.get_doc("Ledger Merge", docname).start_merge()


def start_merge(docname):
	ledger_merge = dontmanage.get_doc("Ledger Merge", docname)
	successful_merges = 0
	total = len(ledger_merge.merge_accounts)
	for row in ledger_merge.merge_accounts:
		if not row.merged:
			try:
				merge_account(
					row.account,
					ledger_merge.account,
				)
				row.db_set("merged", 1)
				dontmanage.db.commit()
				successful_merges += 1
				dontmanage.publish_realtime(
					"ledger_merge_progress",
					{"ledger_merge": ledger_merge.name, "current": successful_merges, "total": total},
				)
			except Exception:
				dontmanage.db.rollback()
				ledger_merge.log_error("Ledger merge failed")
			finally:
				if successful_merges == total:
					ledger_merge.db_set("status", "Success")
				elif successful_merges > 0:
					ledger_merge.db_set("status", "Partial Success")
				else:
					ledger_merge.db_set("status", "Error")

	dontmanage.publish_realtime("ledger_merge_refresh", {"ledger_merge": ledger_merge.name})
