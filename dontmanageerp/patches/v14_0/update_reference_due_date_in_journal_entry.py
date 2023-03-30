import dontmanage


def execute():
	if dontmanage.db.get_value("Journal Entry Account", {"reference_due_date": ""}):
		dontmanage.db.sql(
			"""
			UPDATE `tabJournal Entry Account`
			SET reference_due_date = NULL
			WHERE reference_due_date = ''
		"""
		)
