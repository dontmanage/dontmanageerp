import dontmanage


def execute():
	loan = dontmanage.qb.DocType("Loan")
	loan_type = dontmanage.qb.DocType("Loan Type")

	dontmanage.qb.update(loan_type).set(
		loan_type.repayment_schedule_type, "Monthly as per repayment start date"
	).where(loan_type.is_term_loan == 1).run()

	dontmanage.qb.update(loan).set(
		loan.repayment_schedule_type, "Monthly as per repayment start date"
	).where(loan.is_term_loan == 1).run()
