# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document


class QualityReview(Document):
	def validate(self):
		# fetch targets from goal
		if not self.reviews:
			for d in dontmanage.get_doc("Quality Goal", self.goal).objectives:
				self.append("reviews", dict(objective=d.objective, target=d.target, uom=d.uom))

		self.set_status()

	def set_status(self):
		# if any child item is failed, fail the parent
		if not len(self.reviews or []) or any([d.status == "Open" for d in self.reviews]):
			self.status = "Open"
		elif any([d.status == "Failed" for d in self.reviews]):
			self.status = "Failed"
		else:
			self.status = "Passed"


def review():
	day = dontmanage.utils.getdate().day
	weekday = dontmanage.utils.getdate().strftime("%A")
	month = dontmanage.utils.getdate().strftime("%B")

	for goal in dontmanage.get_list("Quality Goal", fields=["name", "frequency", "date", "weekday"]):
		if goal.frequency == "Daily":
			create_review(goal.name)

		elif goal.frequency == "Weekly" and goal.weekday == weekday:
			create_review(goal.name)

		elif goal.frequency == "Monthly" and goal.date == str(day):
			create_review(goal.name)

		elif goal.frequency == "Quarterly" and day == 1 and get_quarter(month):
			create_review(goal.name)


def create_review(goal):
	goal = dontmanage.get_doc("Quality Goal", goal)

	review = dontmanage.get_doc(
		{"doctype": "Quality Review", "goal": goal.name, "date": dontmanage.utils.getdate()}
	)

	review.insert(ignore_permissions=True)


def get_quarter(month):
	if month in ["January", "April", "July", "October"]:
		return True
	else:
		return False
