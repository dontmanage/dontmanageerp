# Copyright (c) 2018, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.utils.nestedset import NestedSet


class QualityProcedure(NestedSet):
	nsm_parent_field = "parent_quality_procedure"

	def before_save(self):
		self.check_for_incorrect_child()

	def on_update(self):
		NestedSet.on_update(self)
		self.set_parent()

	def after_insert(self):
		self.set_parent()

		# add child to parent if missing
		if self.parent_quality_procedure:
			parent = dontmanage.get_doc("Quality Procedure", self.parent_quality_procedure)
			if not [d for d in parent.processes if d.procedure == self.name]:
				parent.append("processes", {"procedure": self.name, "process_description": self.name})
				parent.save()

	def on_trash(self):
		# clear from child table (sub procedures)
		dontmanage.db.sql(
			"""update `tabQuality Procedure Process`
			set `procedure`='' where `procedure`=%s""",
			self.name,
		)
		NestedSet.on_trash(self, allow_root_deletion=True)

	def set_parent(self):
		for process in self.processes:
			# Set parent for only those children who don't have a parent
			has_parent = dontmanage.db.get_value(
				"Quality Procedure", process.procedure, "parent_quality_procedure"
			)
			if not has_parent and process.procedure:
				dontmanage.db.set_value(self.doctype, process.procedure, "parent_quality_procedure", self.name)

	def check_for_incorrect_child(self):
		for process in self.processes:
			if process.procedure:
				self.is_group = 1
				# Check if any child process belongs to another parent.
				parent_quality_procedure = dontmanage.db.get_value(
					"Quality Procedure", process.procedure, "parent_quality_procedure"
				)
				if parent_quality_procedure and parent_quality_procedure != self.name:
					dontmanage.throw(
						_("{0} already has a Parent Procedure {1}.").format(
							dontmanage.bold(process.procedure), dontmanage.bold(parent_quality_procedure)
						),
						title=_("Invalid Child Procedure"),
					)


@dontmanage.whitelist()
def get_children(doctype, parent=None, parent_quality_procedure=None, is_root=False):
	if parent is None or parent == "All Quality Procedures":
		parent = ""

	if parent:
		parent_procedure = dontmanage.get_doc("Quality Procedure", parent)
		# return the list in order
		return [
			dict(
				value=d.procedure, expandable=dontmanage.db.get_value("Quality Procedure", d.procedure, "is_group")
			)
			for d in parent_procedure.processes
			if d.procedure
		]
	else:
		return dontmanage.get_all(
			"Quality Procedure",
			fields=["name as value", "is_group as expandable"],
			filters=dict(parent_quality_procedure=parent),
			order_by="name asc",
		)


@dontmanage.whitelist()
def add_node():
	from dontmanage.desk.treeview import make_tree_args

	args = dontmanage.form_dict
	args = make_tree_args(**args)

	if args.parent_quality_procedure == "All Quality Procedures":
		args.parent_quality_procedure = None

	return dontmanage.get_doc(args).insert()
