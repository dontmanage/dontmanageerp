# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage


def execute():
	for doctype in ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]:
		tab = dontmanage.qb.DocType(doctype).as_("tab")
		dontmanage.qb.update(tab).set(tab.is_old_subcontracting_flow, 1).where(
			tab.is_subcontracted == 1
		).run()
