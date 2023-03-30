import dontmanage


def execute():
	dontmanage.reload_doc("setup", "doctype", "currency_exchange")
	dontmanage.db.sql("""update `tabCurrency Exchange` set for_buying = 1, for_selling = 1""")
