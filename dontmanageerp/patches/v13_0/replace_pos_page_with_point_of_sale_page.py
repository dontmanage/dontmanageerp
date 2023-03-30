import dontmanage


def execute():
	if dontmanage.db.exists("Page", "point-of-sale"):
		dontmanage.rename_doc("Page", "pos", "point-of-sale", 1, 1)
