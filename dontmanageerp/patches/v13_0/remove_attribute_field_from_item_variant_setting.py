import dontmanage


def execute():
	"""Remove has_variants and attribute fields from item variant settings."""
	dontmanage.reload_doc("stock", "doctype", "Item Variant Settings")

	dontmanage.db.sql(
		"""delete from `tabVariant Field`
			where field_name in ('attributes', 'has_variants')"""
	)
