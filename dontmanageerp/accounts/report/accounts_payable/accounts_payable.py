# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


from dontmanageerp.accounts.report.accounts_receivable.accounts_receivable import ReceivablePayableReport


def execute(filters=None):
	args = {
		"party_type": "Supplier",
		"naming_by": ["Buying Settings", "supp_master_name"],
	}
	return ReceivablePayableReport(filters).run(args)
