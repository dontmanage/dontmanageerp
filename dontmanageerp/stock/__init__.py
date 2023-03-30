import dontmanage
from dontmanage import _

install_docs = [
	{"doctype": "Role", "role_name": "Stock Manager", "name": "Stock Manager"},
	{"doctype": "Role", "role_name": "Item Manager", "name": "Item Manager"},
	{"doctype": "Role", "role_name": "Stock User", "name": "Stock User"},
	{"doctype": "Role", "role_name": "Quality Manager", "name": "Quality Manager"},
	{"doctype": "Item Group", "item_group_name": "All Item Groups", "is_group": 1},
	{
		"doctype": "Item Group",
		"item_group_name": "Default",
		"parent_item_group": "All Item Groups",
		"is_group": 0,
	},
]


def get_warehouse_account_map(company=None):
	company_warehouse_account_map = company and dontmanage.flags.setdefault(
		"warehouse_account_map", {}
	).get(company)
	warehouse_account_map = dontmanage.flags.warehouse_account_map

	if not warehouse_account_map or not company_warehouse_account_map or dontmanage.flags.in_test:
		warehouse_account = dontmanage._dict()

		filters = {}
		if company:
			filters["company"] = company
			dontmanage.flags.setdefault("warehouse_account_map", {}).setdefault(company, {})

		for d in dontmanage.get_all(
			"Warehouse",
			fields=["name", "account", "parent_warehouse", "company", "is_group"],
			filters=filters,
			order_by="lft, rgt",
		):
			if not d.account:
				d.account = get_warehouse_account(d, warehouse_account)

			if d.account:
				d.account_currency = dontmanage.db.get_value("Account", d.account, "account_currency", cache=True)
				warehouse_account.setdefault(d.name, d)
		if company:
			dontmanage.flags.warehouse_account_map[company] = warehouse_account
		else:
			dontmanage.flags.warehouse_account_map = warehouse_account

	return dontmanage.flags.warehouse_account_map.get(company) or dontmanage.flags.warehouse_account_map


def get_warehouse_account(warehouse, warehouse_account=None):
	account = warehouse.account
	if not account and warehouse.parent_warehouse:
		if warehouse_account:
			if warehouse_account.get(warehouse.parent_warehouse):
				account = warehouse_account.get(warehouse.parent_warehouse).account
			else:
				from dontmanage.utils.nestedset import rebuild_tree

				rebuild_tree("Warehouse", "parent_warehouse")
		else:
			account = dontmanage.db.sql(
				"""
				select
					account from `tabWarehouse`
				where
					lft <= %s and rgt >= %s and company = %s
					and account is not null and ifnull(account, '') !=''
				order by lft desc limit 1""",
				(warehouse.lft, warehouse.rgt, warehouse.company),
				as_list=1,
			)

			account = account[0][0] if account else None

	if not account and warehouse.company:
		account = get_company_default_inventory_account(warehouse.company)

	if not account and warehouse.company:
		account = dontmanage.db.get_value(
			"Account", {"account_type": "Stock", "is_group": 0, "company": warehouse.company}, "name"
		)

	if not account and warehouse.company and not warehouse.is_group:
		dontmanage.throw(
			_("Please set Account in Warehouse {0} or Default Inventory Account in Company {1}").format(
				warehouse.name, warehouse.company
			)
		)
	return account


def get_company_default_inventory_account(company):
	return dontmanage.get_cached_value("Company", company, "default_inventory_account")
