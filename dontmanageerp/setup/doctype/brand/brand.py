# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt


import copy

import dontmanage
from dontmanage.model.document import Document


class Brand(Document):
	pass


def get_brand_defaults(item, company):
	item = dontmanage.get_cached_doc("Item", item)
	if item.brand:
		brand = dontmanage.get_cached_doc("Brand", item.brand)

		for d in brand.brand_defaults or []:
			if d.company == company:
				row = copy.deepcopy(d.as_dict())
				row.pop("name")
				return row

	return dontmanage._dict()
