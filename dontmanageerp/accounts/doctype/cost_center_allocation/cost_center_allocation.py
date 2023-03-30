# Copyright (c) 2022, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import add_days, format_date, getdate


class MainCostCenterCantBeChild(dontmanage.ValidationError):
	pass


class InvalidMainCostCenter(dontmanage.ValidationError):
	pass


class InvalidChildCostCenter(dontmanage.ValidationError):
	pass


class WrongPercentageAllocation(dontmanage.ValidationError):
	pass


class InvalidDateError(dontmanage.ValidationError):
	pass


class CostCenterAllocation(Document):
	def __init__(self, *args, **kwargs):
		super(CostCenterAllocation, self).__init__(*args, **kwargs)
		self._skip_from_date_validation = False

	def validate(self):
		self.validate_total_allocation_percentage()
		if not self._skip_from_date_validation:
			self.validate_from_date_based_on_existing_gle()
		self.validate_backdated_allocation()
		self.validate_main_cost_center()
		self.validate_child_cost_centers()

	def validate_total_allocation_percentage(self):
		total_percentage = sum([d.percentage for d in self.get("allocation_percentages", [])])

		if total_percentage != 100:
			dontmanage.throw(
				_("Total percentage against cost centers should be 100"), WrongPercentageAllocation
			)

	def validate_from_date_based_on_existing_gle(self):
		# Check if GLE exists against the main cost center
		# If exists ensure from date is set after posting date of last GLE

		last_gle_date = dontmanage.db.get_value(
			"GL Entry",
			{"cost_center": self.main_cost_center, "is_cancelled": 0},
			"posting_date",
			order_by="posting_date desc",
		)

		if last_gle_date:
			if getdate(self.valid_from) <= getdate(last_gle_date):
				dontmanage.throw(
					_(
						"Valid From must be after {0} as last GL Entry against the cost center {1} posted on this date"
					).format(last_gle_date, self.main_cost_center),
					InvalidDateError,
				)

	def validate_backdated_allocation(self):
		# Check if there are any future existing allocation records against the main cost center
		# If exists, warn the user about it

		future_allocation = dontmanage.db.get_value(
			"Cost Center Allocation",
			filters={
				"main_cost_center": self.main_cost_center,
				"valid_from": (">=", self.valid_from),
				"name": ("!=", self.name),
				"docstatus": 1,
			},
			fieldname=["valid_from", "name"],
			order_by="valid_from",
			as_dict=1,
		)

		if future_allocation:
			dontmanage.msgprint(
				_(
					"Another Cost Center Allocation record {0} applicable from {1}, hence this allocation will be applicable upto {2}"
				).format(
					dontmanage.bold(future_allocation.name),
					dontmanage.bold(format_date(future_allocation.valid_from)),
					dontmanage.bold(format_date(add_days(future_allocation.valid_from, -1))),
				),
				title=_("Warning!"),
				indicator="orange",
				alert=1,
			)

	def validate_main_cost_center(self):
		# Main cost center itself cannot be entered in child table
		if self.main_cost_center in [d.cost_center for d in self.allocation_percentages]:
			dontmanage.throw(
				_("Main Cost Center {0} cannot be entered in the child table").format(self.main_cost_center),
				MainCostCenterCantBeChild,
			)

		# If main cost center is used for allocation under any other cost center,
		# allocation cannot be done against it
		parent = dontmanage.db.get_value(
			"Cost Center Allocation Percentage",
			filters={"cost_center": self.main_cost_center, "docstatus": 1},
			fieldname="parent",
		)
		if parent:
			dontmanage.throw(
				_(
					"{0} cannot be used as a Main Cost Center because it has been used as child in Cost Center Allocation {1}"
				).format(self.main_cost_center, parent),
				InvalidMainCostCenter,
			)

	def validate_child_cost_centers(self):
		# Check if child cost center is used as main cost center in any existing allocation
		main_cost_centers = [
			d.main_cost_center
			for d in dontmanage.get_all("Cost Center Allocation", {"docstatus": 1}, "main_cost_center")
		]

		for d in self.allocation_percentages:
			if d.cost_center in main_cost_centers:
				dontmanage.throw(
					_(
						"Cost Center {0} cannot be used for allocation as it is used as main cost center in other allocation record."
					).format(d.cost_center),
					InvalidChildCostCenter,
				)
