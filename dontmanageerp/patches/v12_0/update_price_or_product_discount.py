import dontmanage


def execute():
	dontmanage.reload_doc("accounts", "doctype", "pricing_rule")

	dontmanage.db.sql(
		""" UPDATE `tabPricing Rule` SET price_or_product_discount = 'Price'
		WHERE ifnull(price_or_product_discount,'') = '' """
	)
