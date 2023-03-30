# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

from datetime import date

import dontmanage
from dontmanage.model.document import Document

from dontmanageerp.utilities.bulk_transaction import task, update_logger


class BulkTransactionLog(Document):
	pass


@dontmanage.whitelist()
def retry_failing_transaction(log_date=None):
	if not log_date:
		log_date = str(date.today())
	btp = dontmanage.qb.DocType("Bulk Transaction Log Detail")
	data = (
		dontmanage.qb.from_(btp)
		.select(btp.transaction_name, btp.from_doctype, btp.to_doctype)
		.distinct()
		.where(btp.retried != 1)
		.where(btp.transaction_status == "Failed")
		.where(btp.date == log_date)
	).run(as_dict=True)

	if data:
		if len(data) > 10:
			dontmanage.enqueue(job, queue="long", job_name="bulk_retry", data=data, log_date=log_date)
		else:
			job(data, log_date)
	else:
		return "No Failed Records"


def job(data, log_date):
	for d in data:
		failed = []
		try:
			dontmanage.db.savepoint("before_creation_of_record")
			task(d.transaction_name, d.from_doctype, d.to_doctype)
		except Exception as e:
			dontmanage.db.rollback(save_point="before_creation_of_record")
			failed.append(e)
			update_logger(
				d.transaction_name,
				e,
				d.from_doctype,
				d.to_doctype,
				status="Failed",
				log_date=log_date,
				restarted=1,
			)

		if not failed:
			update_logger(
				d.transaction_name,
				None,
				d.from_doctype,
				d.to_doctype,
				status="Success",
				log_date=log_date,
				restarted=1,
			)
