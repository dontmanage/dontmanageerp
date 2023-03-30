# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.utils.dashboard import cache_source

from dontmanageerp.loan_management.report.applicant_wise_loan_security_exposure.applicant_wise_loan_security_exposure import (
	get_loan_security_details,
)


@dontmanage.whitelist()
@cache_source
def get_data(
	chart_name=None,
	chart=None,
	no_cache=None,
	filters=None,
	from_date=None,
	to_date=None,
	timespan=None,
	time_interval=None,
	heatmap_year=None,
):
	if chart_name:
		chart = dontmanage.get_doc("Dashboard Chart", chart_name)
	else:
		chart = dontmanage._dict(dontmanage.parse_json(chart))

	filters = {}
	current_pledges = {}

	if filters:
		filters = dontmanage.parse_json(filters)[0]

	conditions = ""
	labels = []
	values = []

	if filters.get("company"):
		conditions = "AND company = %(company)s"

	loan_security_details = get_loan_security_details()

	unpledges = dontmanage._dict(
		dontmanage.db.sql(
			"""
		SELECT u.loan_security, sum(u.qty) as qty
		FROM `tabLoan Security Unpledge` up, `tabUnpledge` u
		WHERE u.parent = up.name
		AND up.status = 'Approved'
		{conditions}
		GROUP BY u.loan_security
	""".format(
				conditions=conditions
			),
			filters,
			as_list=1,
		)
	)

	pledges = dontmanage._dict(
		dontmanage.db.sql(
			"""
		SELECT p.loan_security, sum(p.qty) as qty
		FROM `tabLoan Security Pledge` lp, `tabPledge`p
		WHERE p.parent = lp.name
		AND lp.status = 'Pledged'
		{conditions}
		GROUP BY p.loan_security
	""".format(
				conditions=conditions
			),
			filters,
			as_list=1,
		)
	)

	for security, qty in pledges.items():
		current_pledges.setdefault(security, qty)
		current_pledges[security] -= unpledges.get(security, 0.0)

	sorted_pledges = dict(sorted(current_pledges.items(), key=lambda item: item[1], reverse=True))

	count = 0
	for security, qty in sorted_pledges.items():
		values.append(qty * loan_security_details.get(security, {}).get("latest_price", 0))
		labels.append(security)
		count += 1

		## Just need top 10 securities
		if count == 10:
			break

	return {
		"labels": labels,
		"datasets": [{"name": "Top 10 Securities", "chartType": "bar", "values": values}],
	}
