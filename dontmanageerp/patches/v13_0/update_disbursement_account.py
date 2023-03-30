import dontmanage


def execute():

	dontmanage.reload_doc("loan_management", "doctype", "loan_type")
	dontmanage.reload_doc("loan_management", "doctype", "loan")

	loan_type = dontmanage.qb.DocType("Loan Type")
	loan = dontmanage.qb.DocType("Loan")

	dontmanage.qb.update(loan_type).set(loan_type.disbursement_account, loan_type.payment_account).run()

	dontmanage.qb.update(loan).set(loan.disbursement_account, loan.payment_account).run()
