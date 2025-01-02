# Copyright (c) 2023, DontManage and Contributors
# License: MIT. See LICENSE


import dontmanage
from pypika.terms import ExistsCriterion


def execute():
	pl = dontmanage.qb.DocType("Pick List")
	se = dontmanage.qb.DocType("Stock Entry")
	dn = dontmanage.qb.DocType("Delivery Note")

	(
		dontmanage.qb.update(pl).set(
			pl.status,
			(
				dontmanage.qb.terms.Case()
				.when(pl.docstatus == 0, "Draft")
				.when(pl.docstatus == 2, "Cancelled")
				.else_("Completed")
			),
		)
	).run()

	(
		dontmanage.qb.update(pl)
		.set(pl.status, "Open")
		.where(
			(
				ExistsCriterion(
					dontmanage.qb.from_(se).select(se.name).where((se.docstatus == 1) & (se.pick_list == pl.name))
				)
				| ExistsCriterion(
					dontmanage.qb.from_(dn).select(dn.name).where((dn.docstatus == 1) & (dn.pick_list == pl.name))
				)
			).negate()
			& (pl.docstatus == 1)
		)
	).run()
