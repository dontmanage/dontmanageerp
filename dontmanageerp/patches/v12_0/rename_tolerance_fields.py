import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	dontmanage.reload_doc("stock", "doctype", "item")
	dontmanage.reload_doc("stock", "doctype", "stock_settings")
	dontmanage.reload_doc("accounts", "doctype", "accounts_settings")

	rename_field("Stock Settings", "tolerance", "over_delivery_receipt_allowance")
	rename_field("Item", "tolerance", "over_delivery_receipt_allowance")

	qty_allowance = dontmanage.db.get_single_value("Stock Settings", "over_delivery_receipt_allowance")
	dontmanage.db.set_single_value("Accounts Settings", "over_delivery_receipt_allowance", qty_allowance)

	dontmanage.db.sql("update tabItem set over_billing_allowance=over_delivery_receipt_allowance")
