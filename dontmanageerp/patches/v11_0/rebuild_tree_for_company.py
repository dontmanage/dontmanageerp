import dontmanage
from dontmanage.utils.nestedset import rebuild_tree


def execute():
	dontmanage.reload_doc("setup", "doctype", "company")
	rebuild_tree("Company", "parent_company")
