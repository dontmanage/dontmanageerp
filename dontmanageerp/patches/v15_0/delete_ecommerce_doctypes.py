import click
import dontmanage


def execute():
	if "webshop" in dontmanage.get_installed_apps():
		return

	if not dontmanage.db.table_exists("Website Item"):
		return

	doctypes = [
		"E Commerce Settings",
		"Website Item",
		"Recommended Items",
		"Item Review",
		"Wishlist Item",
		"Wishlist",
		"Website Offer",
		"Website Item Tabbed Section",
	]

	for doctype in doctypes:
		dontmanage.delete_doc("DocType", doctype, ignore_missing=True)

	click.secho(
		"ECommerce is renamed and moved to a separate app"
		"Please install the app for ECommerce features: https://github.com/dontmanage/webshop",
		fg="yellow",
	)
