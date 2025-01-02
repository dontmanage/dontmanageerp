import dontmanage


def execute():
	process_statement_of_accounts = dontmanage.qb.DocType("Process Statement Of Accounts")

	data = (
		dontmanage.qb.from_(process_statement_of_accounts)
		.select(process_statement_of_accounts.name, process_statement_of_accounts.cc_to)
		.where(process_statement_of_accounts.cc_to.isnotnull())
	).run(as_dict=True)

	for d in data:
		doc = dontmanage.get_doc("Process Statement Of Accounts", d.name)
		doc.append("cc_to", {"cc": d.cc_to})
		doc.save()
