# Copyright (c) 2015, DontManage and Contributors and contributors
# For license information, please see license.txt


import dontmanage
from dateutil.relativedelta import relativedelta
from dontmanage.model.document import Document
from dontmanage.utils import cint


class ManufacturingSettings(Document):
	pass


def get_mins_between_operations():
	return relativedelta(
		minutes=cint(dontmanage.db.get_single_value("Manufacturing Settings", "mins_between_operations"))
		or 10
	)


@dontmanage.whitelist()
def is_material_consumption_enabled():
	if not hasattr(dontmanage.local, "material_consumption"):
		dontmanage.local.material_consumption = cint(
			dontmanage.db.get_single_value("Manufacturing Settings", "material_consumption")
		)

	return dontmanage.local.material_consumption
