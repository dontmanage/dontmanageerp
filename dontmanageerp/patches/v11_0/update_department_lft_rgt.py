import dontmanage
from dontmanage import _
from dontmanage.utils.nestedset import rebuild_tree


def execute():
	"""assign lft and rgt appropriately"""
	dontmanage.reload_doc("setup", "doctype", "department")
	if not dontmanage.db.exists("Department", _("All Departments")):
		dontmanage.get_doc(
			{"doctype": "Department", "department_name": _("All Departments"), "is_group": 1}
		).insert(ignore_permissions=True, ignore_mandatory=True)

	dontmanage.db.sql(
		"""update `tabDepartment` set parent_department = '{0}'
		where is_group = 0""".format(
			_("All Departments")
		)
	)

	rebuild_tree("Department", "parent_department")
