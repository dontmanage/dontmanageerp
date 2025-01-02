""" smoak tests to check basic functionality calls on known form loads."""

import dontmanage
from dontmanage.desk.form.load import getdoc
from dontmanage.tests.utils import DontManageTestCase, change_settings
from dontmanage.www.printview import get_html_and_style


class TestFormLoads(DontManageTestCase):
	@change_settings("Print Settings", {"allow_print_for_cancelled": 1})
	def test_load(self):
		dontmanageerp_modules = dontmanage.get_all("Module Def", filters={"app_name": "dontmanageerp"}, pluck="name")
		doctypes = dontmanage.get_all(
			"DocType",
			{"istable": 0, "issingle": 0, "is_virtual": 0, "module": ("in", dontmanageerp_modules)},
			pluck="name",
		)

		for doctype in doctypes:
			last_doc = dontmanage.db.get_value(doctype, {}, "name", order_by="modified desc")
			if not last_doc:
				continue
			with self.subTest(msg=f"Loading {doctype} - {last_doc}", doctype=doctype, last_doc=last_doc):
				self.assertFormLoad(doctype, last_doc)
				self.assertDocPrint(doctype, last_doc)

	def assertFormLoad(self, doctype, docname):
		# reset previous response
		dontmanage.response = dontmanage._dict({"docs": []})
		dontmanage.response.docinfo = None

		try:
			getdoc(doctype, docname)
		except Exception as e:
			self.fail(f"Failed to load {doctype}-{docname}: {e}")

		self.assertTrue(
			dontmanage.response.docs, msg=f"expected document in reponse, found: {dontmanage.response.docs}"
		)
		self.assertTrue(
			dontmanage.response.docinfo, msg=f"expected docinfo in reponse, found: {dontmanage.response.docinfo}"
		)

	def assertDocPrint(self, doctype, docname):
		doc = dontmanage.get_doc(doctype, docname)
		doc.set("__onload", dontmanage._dict())
		doc.run_method("onload")

		messages_before = dontmanage.get_message_log()
		ret = get_html_and_style(doc=doc.as_json(), print_format="Standard", no_letterhead=1)
		messages_after = dontmanage.get_message_log()

		if len(messages_after) > len(messages_before):
			new_messages = messages_after[len(messages_before) :]
			self.fail("Print view showing error/warnings: \n" + "\n".join(str(msg) for msg in new_messages))

		# html should exist
		self.assertTrue(bool(ret["html"]))
