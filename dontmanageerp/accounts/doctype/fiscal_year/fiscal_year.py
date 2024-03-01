# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dateutil.relativedelta import relativedelta
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import add_days, add_years, cstr, getdate


class FiscalYear(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.fiscal_year_company.fiscal_year_company import FiscalYearCompany

		auto_created: DF.Check
		companies: DF.Table[FiscalYearCompany]
		disabled: DF.Check
		is_short_year: DF.Check
		year: DF.Data
		year_end_date: DF.Date
		year_start_date: DF.Date
	# end: auto-generated types

	def validate(self):
		self.validate_dates()
		self.validate_overlap()

		if not self.is_new():
			year_start_end_dates = dontmanage.db.sql(
				"""select year_start_date, year_end_date
				from `tabFiscal Year` where name=%s""",
				(self.name),
			)

			if year_start_end_dates:
				if (
					getdate(self.year_start_date) != year_start_end_dates[0][0]
					or getdate(self.year_end_date) != year_start_end_dates[0][1]
				):
					dontmanage.throw(
						_(
							"Cannot change Fiscal Year Start Date and Fiscal Year End Date once the Fiscal Year is saved."
						)
					)

	def validate_dates(self):
		self.validate_from_to_dates("year_start_date", "year_end_date")
		if self.is_short_year:
			# Fiscal Year can be shorter than one year, in some jurisdictions
			# under certain circumstances. For example, in the USA and Germany.
			return

		date = getdate(self.year_start_date) + relativedelta(years=1) - relativedelta(days=1)

		if getdate(self.year_end_date) != date:
			dontmanage.throw(
				_("Fiscal Year End Date should be one year after Fiscal Year Start Date"),
				dontmanage.exceptions.InvalidDates,
			)

	def on_update(self):
		check_duplicate_fiscal_year(self)
		dontmanage.cache().delete_value("fiscal_years")

	def on_trash(self):
		dontmanage.cache().delete_value("fiscal_years")

	def validate_overlap(self):
		existing_fiscal_years = dontmanage.db.sql(
			"""select name from `tabFiscal Year`
			where (
				(%(year_start_date)s between year_start_date and year_end_date)
				or (%(year_end_date)s between year_start_date and year_end_date)
				or (year_start_date between %(year_start_date)s and %(year_end_date)s)
				or (year_end_date between %(year_start_date)s and %(year_end_date)s)
			) and name!=%(name)s""",
			{
				"year_start_date": self.year_start_date,
				"year_end_date": self.year_end_date,
				"name": self.name or "No Name",
			},
			as_dict=True,
		)

		if existing_fiscal_years:
			for existing in existing_fiscal_years:
				company_for_existing = dontmanage.db.sql_list(
					"""select company from `tabFiscal Year Company`
					where parent=%s""",
					existing.name,
				)

				overlap = False
				if not self.get("companies") or not company_for_existing:
					overlap = True

				for d in self.get("companies"):
					if d.company in company_for_existing:
						overlap = True

				if overlap:
					dontmanage.throw(
						_("Year start date or end date is overlapping with {0}. To avoid please set company").format(
							existing.name
						),
						dontmanage.NameError,
					)


@dontmanage.whitelist()
def check_duplicate_fiscal_year(doc):
	year_start_end_dates = dontmanage.db.sql(
		"""select name, year_start_date, year_end_date from `tabFiscal Year` where name!=%s""",
		(doc.name),
	)
	for fiscal_year, ysd, yed in year_start_end_dates:
		if (getdate(doc.year_start_date) == ysd and getdate(doc.year_end_date) == yed) and (
			not dontmanage.flags.in_test
		):
			dontmanage.throw(
				_("Fiscal Year Start Date and Fiscal Year End Date are already set in Fiscal Year {0}").format(
					fiscal_year
				)
			)


@dontmanage.whitelist()
def auto_create_fiscal_year():
	for d in dontmanage.db.sql(
		"""select name from `tabFiscal Year` where year_end_date = date_add(current_date, interval 3 day)"""
	):
		try:
			current_fy = dontmanage.get_doc("Fiscal Year", d[0])

			new_fy = dontmanage.copy_doc(current_fy, ignore_no_copy=False)

			new_fy.year_start_date = add_days(current_fy.year_end_date, 1)
			new_fy.year_end_date = add_years(current_fy.year_end_date, 1)

			start_year = cstr(new_fy.year_start_date.year)
			end_year = cstr(new_fy.year_end_date.year)
			new_fy.year = start_year if start_year == end_year else (start_year + "-" + end_year)
			new_fy.auto_created = 1

			new_fy.insert(ignore_permissions=True)
		except dontmanage.NameError:
			pass


def get_from_and_to_date(fiscal_year):
	fields = ["year_start_date", "year_end_date"]
	cached_results = dontmanage.get_cached_value("Fiscal Year", fiscal_year, fields, as_dict=1)
	return dict(from_date=cached_results.year_start_date, to_date=cached_results.year_end_date)