import click
import dontmanage


def execute():
	if "lending" in dontmanage.get_installed_apps():
		return

	click.secho(
		"Loan Management module has been moved to a separate app"
		" and will be removed from DontManageErp in Version 15."
		" Please install the Lending app when upgrading to Version 15"
		" to continue using the Loan Management module:\n"
		"https://github.com/dontmanage/lending",
		fg="yellow",
	)
