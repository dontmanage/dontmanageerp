# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage
from dontmanage import _

from dontmanageerp.e_commerce.doctype.e_commerce_settings.e_commerce_settings import show_attachments


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = dontmanage.get_doc(dontmanage.form_dict.doctype, dontmanage.form_dict.name)
	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	if show_attachments():
		context.attachments = get_attachments(dontmanage.form_dict.doctype, dontmanage.form_dict.name)

	context.parents = dontmanage.form_dict.parents
	context.title = dontmanage.form_dict.name
	context.payment_ref = dontmanage.db.get_value(
		"Payment Request", {"reference_name": dontmanage.form_dict.name}, "name"
	)

	context.enabled_checkout = dontmanage.get_doc("E Commerce Settings").enable_checkout

	default_print_format = dontmanage.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=dontmanage.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	if not dontmanage.has_website_permission(context.doc):
		dontmanage.throw(_("Not Permitted"), dontmanage.PermissionError)

	context.available_loyalty_points = 0.0
	if context.doc.get("customer"):
		# check for the loyalty program of the customer
		customer_loyalty_program = dontmanage.db.get_value(
			"Customer", context.doc.customer, "loyalty_program"
		)

		if customer_loyalty_program:
			from dontmanageerp.accounts.doctype.loyalty_program.loyalty_program import (
				get_loyalty_program_details_with_points,
			)

			loyalty_program_details = get_loyalty_program_details_with_points(
				context.doc.customer, customer_loyalty_program
			)
			context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

	context.show_pay_button = dontmanage.db.get_single_value("Buying Settings", "show_pay_button")
	context.show_make_pi_button = False
	if context.doc.get("supplier"):
		# show Make Purchase Invoice button based on permission
		context.show_make_pi_button = dontmanage.has_permission("Purchase Invoice", "create")


def get_attachments(dt, dn):
	return dontmanage.get_all(
		"File",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)
