import click
import dontmanage


def execute():

	dontmanage.delete_doc("DocType", "Shopping Cart Settings", ignore_missing=True)
	dontmanage.delete_doc("DocType", "Products Settings", ignore_missing=True)
	dontmanage.delete_doc("DocType", "Supplier Item Group", ignore_missing=True)

	if dontmanage.db.get_single_value("E Commerce Settings", "enabled"):
		notify_users()


def notify_users():

	click.secho(
		"Shopping cart and Product settings are merged into E-commerce settings.\n"
		"Checkout the documentation to learn more:"
		"https://docs.dontmanageerp.com/docs/v13/user/manual/en/e_commerce/set_up_e_commerce",
		fg="yellow",
	)

	note = dontmanage.new_doc("Note")
	note.title = "New E-Commerce Module"
	note.public = 1
	note.notify_on_login = 1
	note.content = """<div class="ql-editor read-mode"><p>You are seeing this message because Shopping Cart is enabled on your site. </p><p><br></p><p>Shopping Cart Settings and Products settings are now merged into "E Commerce Settings". </p><p><br></p><p>You can learn about new and improved E-Commerce features in the official documentation.</p><ol><li data-list="bullet"><span class="ql-ui" contenteditable="false"></span><a href="https://docs.dontmanageerp.com/docs/v13/user/manual/en/e_commerce/set_up_e_commerce" rel="noopener noreferrer">https://docs.dontmanageerp.com/docs/v13/user/manual/en/e_commerce/set_up_e_commerce</a></li></ol><p><br></p></div>"""
	note.insert(ignore_mandatory=True)
