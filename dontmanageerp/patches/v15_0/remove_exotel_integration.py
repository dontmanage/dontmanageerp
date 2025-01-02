import click
import dontmanage
from dontmanage import _
from dontmanage.desk.doctype.notification_log.notification_log import make_notification_logs
from dontmanage.utils.user import get_system_managers

SETTINGS_DOCTYPE = "Exotel Settings"


def execute():
	if "exotel_integration" in dontmanage.get_installed_apps():
		return

	try:
		exotel = dontmanage.get_doc(SETTINGS_DOCTYPE)
		if exotel.enabled:
			notify_existing_users()

		dontmanage.delete_doc("DocType", SETTINGS_DOCTYPE)
	except Exception:
		dontmanage.log_error("Failed to remove Exotel Integration.")


def notify_existing_users():
	click.secho(
		"Exotel integration is moved to a separate app and will be removed from DontManageErp in version-15.\n"
		"Please install the app to continue using the integration: https://github.com/dontmanage/exotel_integration",
		fg="yellow",
	)

	notification = {
		"subject": _(
			"WARNING: Exotel app has been separated from DontManageErp, please install the app to continue using Exotel integration."
		),
		"type": "Alert",
	}
	make_notification_logs(notification, get_system_managers(only_name=True))
