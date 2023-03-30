import dontmanage


def execute():
	dontmanage.reload_doc("loan_management", "doctype", "loan")
	loan = dontmanage.qb.DocType("Loan")

	for company in dontmanage.get_all("Company", pluck="name"):
		default_cost_center = dontmanage.db.get_value("Company", company, "cost_center")
		dontmanage.qb.update(loan).set(loan.cost_center, default_cost_center).where(
			loan.company == company
		).run()
