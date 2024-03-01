# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt


from dontmanage.model.document import Document


class MaintenanceTeamMember(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		full_name: DF.Data | None
		maintenance_role: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		team_member: DF.Link
	# end: auto-generated types

	pass
