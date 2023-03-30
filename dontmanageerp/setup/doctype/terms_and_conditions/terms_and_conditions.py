# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import json

import dontmanage
from dontmanage import _, throw
from dontmanage.model.document import Document
from dontmanage.utils import cint
from dontmanage.utils.jinja import validate_template


class TermsandConditions(Document):
	def validate(self):
		if self.terms:
			validate_template(self.terms)
		if (
			not cint(self.buying)
			and not cint(self.selling)
			and not cint(self.hr)
			and not cint(self.disabled)
		):
			throw(_("At least one of the Applicable Modules should be selected"))


@dontmanage.whitelist()
def get_terms_and_conditions(template_name, doc):
	if isinstance(doc, str):
		doc = json.loads(doc)

	terms_and_conditions = dontmanage.get_doc("Terms and Conditions", template_name)

	if terms_and_conditions.terms:
		return dontmanage.render_template(terms_and_conditions.terms, doc)
