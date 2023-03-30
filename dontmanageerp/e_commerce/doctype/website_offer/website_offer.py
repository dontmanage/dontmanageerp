# -*- coding: utf-8 -*-
# Copyright (c) 2021, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class WebsiteOffer(Document):
	pass


@dontmanage.whitelist(allow_guest=True)
def get_offer_details(offer_id):
	return dontmanage.db.get_value("Website Offer", {"name": offer_id}, ["offer_details"])
