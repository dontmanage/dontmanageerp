# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.utils import flt


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = dontmanage.get_doc(dontmanage.form_dict.doctype, dontmanage.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	context.parents = dontmanage.form_dict.parents
	context.title = dontmanage.form_dict.name

	if not dontmanage.has_website_permission(context.doc):
		dontmanage.throw(_("Not Permitted"), dontmanage.PermissionError)

	default_print_format = dontmanage.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=dontmanage.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"
	context.doc.items = get_more_items_info(context.doc.items, context.doc.name)


def get_more_items_info(items, material_request):
	for item in items:
		item.customer_provided = dontmanage.get_value("Item", item.item_code, "is_customer_provided_item")
		item.work_orders = dontmanage.db.sql(
			"""
			select
				wo.name, wo.status, wo_item.consumed_qty
			from
				`tabWork Order Item` wo_item, `tabWork Order` wo
			where
				wo_item.item_code=%s
				and wo_item.consumed_qty=0
				and wo_item.parent=wo.name
				and wo.status not in ('Completed', 'Cancelled', 'Stopped')
			order by
				wo.name asc""",
			item.item_code,
			as_dict=1,
		)
		item.delivered_qty = flt(
			dontmanage.db.sql(
				"""select sum(transfer_qty)
						from `tabStock Entry Detail` where material_request = %s
						and item_code = %s and docstatus = 1""",
				(material_request, item.item_code),
			)[0][0]
		)
	return items
