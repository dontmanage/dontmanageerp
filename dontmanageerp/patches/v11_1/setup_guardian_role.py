import dontmanage


def execute():
	if "Education" in dontmanage.get_active_domains() and not dontmanage.db.exists("Role", "Guardian"):
		doc = dontmanage.new_doc("Role")
		doc.update({"role_name": "Guardian", "desk_access": 0})

		doc.insert(ignore_permissions=True)
