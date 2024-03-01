# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

from datetime import datetime
from typing import Union

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import getdate

from dontmanageerp.accounts.doctype.subscription.subscription import process_all


class ProcessSubscription(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		amended_from: DF.Link | None
		posting_date: DF.Date
		subscription: DF.Link | None
	# end: auto-generated types

	def on_submit(self):
		process_all(subscription=self.subscription, posting_date=self.posting_date)


def create_subscription_process(
	subscription: str | None = None, posting_date: Union[str, datetime.date] | None = None
):
	"""Create a new Process Subscription document"""
	doc = dontmanage.new_doc("Process Subscription")
	doc.subscription = subscription
	doc.posting_date = getdate(posting_date)
	doc.submit()
