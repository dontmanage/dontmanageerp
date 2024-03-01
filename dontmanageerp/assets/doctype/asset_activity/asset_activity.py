# Copyright (c) 2023, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import now_datetime


class AssetActivity(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		asset: DF.Link
		date: DF.Datetime
		subject: DF.SmallText
		user: DF.Link
	# end: auto-generated types

	pass


def add_asset_activity(asset, subject):
	dontmanage.get_doc(
		{
			"doctype": "Asset Activity",
			"asset": asset,
			"subject": subject,
			"user": dontmanage.session.user,
			"date": now_datetime(),
		}
	).insert(ignore_permissions=True, ignore_links=True)
