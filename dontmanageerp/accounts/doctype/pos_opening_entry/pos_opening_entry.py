# Copyright (c) 2020, DontManage and contributors
# For license information, please see license.txt


import dontmanage
from dontmanage import _
from dontmanage.utils import cint, get_link_to_form

from dontmanageerp.controllers.status_updater import StatusUpdater


class POSOpeningEntry(StatusUpdater):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		from dontmanageerp.accounts.doctype.pos_opening_entry_detail.pos_opening_entry_detail import (
			POSOpeningEntryDetail,
		)

		amended_from: DF.Link | None
		balance_details: DF.Table[POSOpeningEntryDetail]
		company: DF.Link
		period_end_date: DF.Date | None
		period_start_date: DF.Datetime
		pos_closing_entry: DF.Data | None
		pos_profile: DF.Link
		posting_date: DF.Date
		set_posting_date: DF.Check
		status: DF.Literal["Draft", "Open", "Closed", "Cancelled"]
		user: DF.Link
	# end: auto-generated types

	def validate(self):
		self.validate_pos_profile_and_cashier()
		self.validate_payment_method_account()
		self.set_status()

	def validate_pos_profile_and_cashier(self):
		if self.company != dontmanage.db.get_value("POS Profile", self.pos_profile, "company"):
			dontmanage.throw(
				_("POS Profile {} does not belongs to company {}").format(self.pos_profile, self.company)
			)

		if not cint(dontmanage.db.get_value("User", self.user, "enabled")):
			dontmanage.throw(_("User {} is disabled. Please select valid user/cashier").format(self.user))

	def validate_payment_method_account(self):
		invalid_modes = []
		for d in self.balance_details:
			if d.mode_of_payment:
				account = dontmanage.db.get_value(
					"Mode of Payment Account",
					{"parent": d.mode_of_payment, "company": self.company},
					"default_account",
				)
				if not account:
					invalid_modes.append(get_link_to_form("Mode of Payment", d.mode_of_payment))

		if invalid_modes:
			if invalid_modes == 1:
				msg = _("Please set default Cash or Bank account in Mode of Payment {}")
			else:
				msg = _("Please set default Cash or Bank account in Mode of Payments {}")
			dontmanage.throw(msg.format(", ".join(invalid_modes)), title=_("Missing Account"))

	def on_submit(self):
		self.set_status(update=True)