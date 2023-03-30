import dontmanage
from dontmanage import _
from dontmanage.model.utils.rename_field import rename_field
from dontmanage.utils.nestedset import rebuild_tree


def execute():
	if dontmanage.db.table_exists("Supplier Group"):
		dontmanage.reload_doc("setup", "doctype", "supplier_group")
	elif dontmanage.db.table_exists("Supplier Type"):
		dontmanage.rename_doc("DocType", "Supplier Type", "Supplier Group", force=True)
		dontmanage.reload_doc("setup", "doctype", "supplier_group")
		dontmanage.reload_doc("accounts", "doctype", "pricing_rule")
		dontmanage.reload_doc("accounts", "doctype", "tax_rule")
		dontmanage.reload_doc("buying", "doctype", "buying_settings")
		dontmanage.reload_doc("buying", "doctype", "supplier")
		rename_field("Supplier Group", "supplier_type", "supplier_group_name")
		rename_field("Supplier", "supplier_type", "supplier_group")
		rename_field("Buying Settings", "supplier_type", "supplier_group")
		rename_field("Pricing Rule", "supplier_type", "supplier_group")
		rename_field("Tax Rule", "supplier_type", "supplier_group")

	build_tree()


def build_tree():
	dontmanage.db.sql(
		"""update `tabSupplier Group` set parent_supplier_group = '{0}'
		where is_group = 0""".format(
			_("All Supplier Groups")
		)
	)

	if not dontmanage.db.exists("Supplier Group", _("All Supplier Groups")):
		dontmanage.get_doc(
			{
				"doctype": "Supplier Group",
				"supplier_group_name": _("All Supplier Groups"),
				"is_group": 1,
				"parent_supplier_group": "",
			}
		).insert(ignore_permissions=True)

	rebuild_tree("Supplier Group", "parent_supplier_group")
