# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.utils.nestedset import NestedSet, get_root_of


class CustomerGroup(NestedSet):
	nsm_parent_field = "parent_customer_group"

	def validate(self):
		if not self.parent_customer_group:
			self.parent_customer_group = get_root_of("Customer Group")

	def on_update(self):
		self.validate_name_with_customer()
		super(CustomerGroup, self).on_update()
		self.validate_one_root()

	def validate_name_with_customer(self):
		if dontmanage.db.exists("Customer", self.name):
			dontmanage.msgprint(_("A customer with the same name already exists"), raise_exception=1)


def get_parent_customer_groups(customer_group):
	lft, rgt = dontmanage.db.get_value("Customer Group", customer_group, ["lft", "rgt"])

	return dontmanage.db.sql(
		"""select name from `tabCustomer Group`
		where lft <= %s and rgt >= %s
		order by lft asc""",
		(lft, rgt),
		as_dict=True,
	)


def on_doctype_update():
	dontmanage.db.add_index("Customer Group", ["lft", "rgt"])
