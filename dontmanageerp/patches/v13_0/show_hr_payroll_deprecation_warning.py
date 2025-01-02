import click
import dontmanage


def execute():
	if "hrms" in dontmanage.get_installed_apps():
		return

	click.secho(
		"HR and Payroll modules have been moved to a separate app"
		" and will be removed from DontManageErp in Version 14."
		" Please install the HRMS app when upgrading to Version 14"
		" to continue using the HR and Payroll modules:\n"
		"https://github.com/dontmanage/hrms",
		fg="yellow",
	)
