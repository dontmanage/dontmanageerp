import click
import dontmanage


def execute():
	table = "tabStock Ledger Entry"
	index = "posting_datetime_creation_index"

	if not dontmanage.db.has_index(table, index):
		return

	try:
		dontmanage.db.sql_ddl(f"ALTER TABLE `{table}` DROP INDEX `{index}`")
		click.echo(f"✓ dropped {index} index from {table}")
	except Exception:
		dontmanage.log_error("Failed to drop index")
