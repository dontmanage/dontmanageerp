# Copyright (c) 2020, DontManage and Contributors
# MIT License. See license.txt


import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if dontmanage.db.has_column("Member", "email"):
		# Get all members
		for member in dontmanage.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not dontmanage.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = dontmanage.db.get_value("Member", member, "email")

				# Set the value for it
				dontmanage.db.set_value("Member", member, "email_id", email)

	if dontmanage.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
