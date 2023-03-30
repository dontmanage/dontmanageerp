# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _, throw
from dontmanage.model.document import Document
from dontmanage.model.mapper import get_mapped_doc

import dontmanageerp.buying.doctype.supplier_scorecard_variable.supplier_scorecard_variable as variable_functions
from dontmanageerp.buying.doctype.supplier_scorecard_criteria.supplier_scorecard_criteria import (
	get_variables,
)


class SupplierScorecardPeriod(Document):
	def validate(self):
		self.validate_criteria_weights()
		self.calculate_variables()
		self.calculate_criteria()
		self.calculate_score()

	def validate_criteria_weights(self):

		weight = 0
		for c in self.criteria:
			weight += c.weight

		if weight != 100:
			throw(_("Criteria weights must add up to 100%"))

	def calculate_variables(self):
		for var in self.variables:
			if "." in var.path:
				method_to_call = import_string_path(var.path)
				var.value = method_to_call(self)
			else:
				method_to_call = getattr(variable_functions, var.path)
				var.value = method_to_call(self)

	def calculate_criteria(self):
		for crit in self.criteria:
			try:
				crit.score = min(
					crit.max_score,
					max(
						0, dontmanage.safe_eval(self.get_eval_statement(crit.formula), None, {"max": max, "min": min})
					),
				)
			except Exception:
				dontmanage.throw(
					_("Could not solve criteria score function for {0}. Make sure the formula is valid.").format(
						crit.criteria_name
					),
					dontmanage.ValidationError,
				)
				crit.score = 0

	def calculate_score(self):
		myscore = 0
		for crit in self.criteria:
			myscore += crit.score * crit.weight / 100.0
		self.total_score = myscore

	def calculate_weighted_score(self, weighing_function):
		try:
			weighed_score = dontmanage.safe_eval(
				self.get_eval_statement(weighing_function), None, {"max": max, "min": min}
			)
		except Exception:
			dontmanage.throw(
				_("Could not solve weighted score function. Make sure the formula is valid."),
				dontmanage.ValidationError,
			)
			weighed_score = 0
		return weighed_score

	def get_eval_statement(self, formula):
		my_eval_statement = formula.replace("\r", "").replace("\n", "")

		for var in self.variables:
			if var.value:
				if var.param_name in my_eval_statement:
					my_eval_statement = my_eval_statement.replace(
						"{" + var.param_name + "}", "{:.2f}".format(var.value)
					)
			else:
				if var.param_name in my_eval_statement:
					my_eval_statement = my_eval_statement.replace("{" + var.param_name + "}", "0.0")

		return my_eval_statement


def import_string_path(path):
	components = path.split(".")
	mod = __import__(components[0])
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod


@dontmanage.whitelist()
def make_supplier_scorecard(source_name, target_doc=None):
	def update_criteria_fields(obj, target, source_parent):
		target.max_score, target.formula = dontmanage.db.get_value(
			"Supplier Scorecard Criteria", obj.criteria_name, ["max_score", "formula"]
		)

	def post_process(source, target):
		variables = []
		for cr in target.criteria:
			for var in get_variables(cr.criteria_name):
				if var not in variables:
					variables.append(var)

		target.extend("variables", variables)

	doc = get_mapped_doc(
		"Supplier Scorecard",
		source_name,
		{
			"Supplier Scorecard": {"doctype": "Supplier Scorecard Period"},
			"Supplier Scorecard Scoring Criteria": {
				"doctype": "Supplier Scorecard Scoring Criteria",
				"postprocess": update_criteria_fields,
			},
		},
		target_doc,
		post_process,
		ignore_permissions=True,
	)

	return doc
