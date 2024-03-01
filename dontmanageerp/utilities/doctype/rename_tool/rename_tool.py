# Copyright (c) 2015, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import dontmanage
from dontmanage.model.document import Document
from dontmanage.model.rename_doc import bulk_rename


class RenameTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from dontmanage.types import DF

		file_to_rename: DF.Attach | None
		select_doctype: DF.Literal
	# end: auto-generated types

	pass


@dontmanage.whitelist()
def get_doctypes():
	return dontmanage.db.sql_list(
		"""select name from tabDocType
		where allow_rename=1 and module!='Core' order by name"""
	)


@dontmanage.whitelist()
def upload(select_doctype=None, rows=None):
	from dontmanage.utils.csvutils import read_csv_content_from_attached_file

	if not select_doctype:
		select_doctype = dontmanage.form_dict.select_doctype

	if not dontmanage.has_permission(select_doctype, "write"):
		raise dontmanage.PermissionError

	rows = read_csv_content_from_attached_file(dontmanage.get_doc("Rename Tool", "Rename Tool"))

	return bulk_rename(select_doctype, rows=rows)
