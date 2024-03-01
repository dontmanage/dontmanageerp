# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage.utils.nestedset import NestedSet, get_root_of

from dontmanageerp.utilities.transaction_base import delete_events


class Department(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		company: DF.Link
		department_name: DF.Data
		disabled: DF.Check
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Data | None
		parent_department: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	nsm_parent_field = "parent_department"

	def autoname(self):
		root = get_root_of("Department")
		if root and self.department_name != root:
			self.name = get_abbreviated_name(self.department_name, self.company)
		else:
			self.name = self.department_name

	def validate(self):
		if not self.parent_department:
			root = get_root_of("Department")
			if root:
				self.parent_department = root

	def before_rename(self, old, new, merge=False):
		# renaming consistency with abbreviation
		if not dontmanage.get_cached_value("Company", self.company, "abbr") in new:
			new = get_abbreviated_name(new, self.company)

		return new

	def on_update(self):
		if not (dontmanage.local.flags.ignore_update_nsm or dontmanage.flags.in_setup_wizard):
			super(Department, self).on_update()

	def on_trash(self):
		super(Department, self).on_trash()
		delete_events(self.doctype, self.name)


def on_doctype_update():
	dontmanage.db.add_index("Department", ["lft", "rgt"])


def get_abbreviated_name(name, company):
	abbr = dontmanage.get_cached_value("Company", company, "abbr")
	new_name = "{0} - {1}".format(name, abbr)
	return new_name


@dontmanage.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	fields = ["name as value", "is_group as expandable"]
	filters = {}

	if company == parent:
		filters["name"] = get_root_of("Department")
	elif company:
		filters["parent_department"] = parent
		filters["company"] = company
	else:
		filters["parent_department"] = parent

	return dontmanage.get_all("Department", fields=fields, filters=filters, order_by="name")


@dontmanage.whitelist()
def add_node():
	from dontmanage.desk.treeview import make_tree_args

	args = dontmanage.form_dict
	args = make_tree_args(**args)

	if args.parent_department == args.company:
		args.parent_department = None

	dontmanage.get_doc(args).insert()
