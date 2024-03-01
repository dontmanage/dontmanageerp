# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import get_link_to_form


class ProductBundle(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.selling.doctype.product_bundle_item.product_bundle_item import ProductBundleItem

		description: DF.Data | None
		disabled: DF.Check
		items: DF.Table[ProductBundleItem]
		new_item_code: DF.Link
	# end: auto-generated types

	def autoname(self):
		self.name = self.new_item_code

	def validate(self):
		self.validate_main_item()
		self.validate_child_items()
		from dontmanageerp.utilities.transaction_base import validate_uom_is_integer

		validate_uom_is_integer(self, "uom", "qty")

	def on_trash(self):
		linked_doctypes = [
			"Delivery Note",
			"Sales Invoice",
			"POS Invoice",
			"Purchase Receipt",
			"Purchase Invoice",
			"Stock Entry",
			"Stock Reconciliation",
			"Sales Order",
			"Purchase Order",
			"Material Request",
		]

		invoice_links = []
		for doctype in linked_doctypes:
			item_doctype = doctype + " Item"

			if doctype == "Stock Entry":
				item_doctype = doctype + " Detail"

			invoices = dontmanage.db.get_all(
				item_doctype, {"item_code": self.new_item_code, "docstatus": 1}, ["parent"]
			)

			for invoice in invoices:
				invoice_links.append(get_link_to_form(doctype, invoice["parent"]))

		if len(invoice_links):
			dontmanage.throw(
				"This Product Bundle is linked with {0}. You will have to cancel these documents in order to delete this Product Bundle".format(
					", ".join(invoice_links)
				),
				title=_("Not Allowed"),
			)

	def validate_main_item(self):
		"""Validates, main Item is not a stock item"""
		if dontmanage.db.get_value("Item", self.new_item_code, "is_stock_item"):
			dontmanage.throw(_("Parent Item {0} must not be a Stock Item").format(self.new_item_code))
		if dontmanage.db.get_value("Item", self.new_item_code, "is_fixed_asset"):
			dontmanage.throw(_("Parent Item {0} must not be a Fixed Asset").format(self.new_item_code))

	def validate_child_items(self):
		for item in self.items:
			if dontmanage.db.exists("Product Bundle", {"name": item.item_code, "disabled": 0}):
				dontmanage.throw(
					_(
						"Row #{0}: Child Item should not be a Product Bundle. Please remove Item {1} and Save"
					).format(item.idx, dontmanage.bold(item.item_code))
				)


@dontmanage.whitelist()
@dontmanage.validate_and_sanitize_search_inputs
def get_new_item_code(doctype, txt, searchfield, start, page_len, filters):
	product_bundles = dontmanage.db.get_list("Product Bundle", {"disabled": 0}, pluck="name")

	item = dontmanage.qb.DocType("Item")
	query = (
		dontmanage.qb.from_(item)
		.select(item.item_code, item.item_name)
		.where(
			(item.is_stock_item == 0) & (item.is_fixed_asset == 0) & (item[searchfield].like(f"%{txt}%"))
		)
		.limit(page_len)
		.offset(start)
	)

	if product_bundles:
		query = query.where(item.name.notin(product_bundles))

	return query.run()
