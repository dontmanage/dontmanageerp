# Copyright (c) 2022, DontManage and Contributors
# License: MIT. See LICENSE

import dontmanage


def execute():
	process_soa = dontmanage.qb.DocType("Process Statement Of Accounts")
	q = dontmanage.qb.update(process_soa).set(process_soa.report, "General Ledger")
	q.run()
