import dontmanage
from dontmanage.model.utils.rename_field import rename_field


def execute():
	if dontmanage.db.has_column("Delivery Stop", "lock"):
		rename_field("Delivery Stop", "lock", "locked")
