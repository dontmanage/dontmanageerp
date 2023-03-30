import dontmanage

from dontmanageerp.setup.install import create_default_success_action


def execute():
	dontmanage.reload_doc("core", "doctype", "success_action")
	create_default_success_action()
