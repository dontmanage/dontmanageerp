import dontmanage


def execute():
	pr_table = dontmanage.qb.DocType("Pricing Rule")
	(
		dontmanage.qb.update(pr_table)
		.set(pr_table.has_priority, 1)
		.where((pr_table.priority.isnotnull()) & (pr_table.priority != ""))
	).run()
