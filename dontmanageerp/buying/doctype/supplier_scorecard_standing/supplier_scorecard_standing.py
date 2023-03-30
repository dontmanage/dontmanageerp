# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class SupplierScorecardStanding(Document):
	pass


@dontmanage.whitelist()
def get_scoring_standing(standing_name):
	standing = dontmanage.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@dontmanage.whitelist()
def get_standings_list():
	standings = dontmanage.db.sql(
		"""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
		{},
		as_dict=1,
	)

	return standings
