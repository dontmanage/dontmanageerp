import dontmanage


def execute():
	dontmanage.reload_doctype("Maintenance Visit")
	dontmanage.reload_doctype("Maintenance Visit Purpose")

	# Updates the Maintenance Schedule link to fetch serial nos
	from dontmanage.query_builder.functions import Coalesce

	mvp = dontmanage.qb.DocType("Maintenance Visit Purpose")
	mv = dontmanage.qb.DocType("Maintenance Visit")

	dontmanage.qb.update(mv).join(mvp).on(mvp.parent == mv.name).set(
		mv.maintenance_schedule, Coalesce(mvp.prevdoc_docname, "")
	).where(
		(mv.maintenance_type == "Scheduled") & (mvp.prevdoc_docname.notnull()) & (mv.docstatus < 2)
	).run(
		as_dict=1
	)
