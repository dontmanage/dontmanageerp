import dontmanage

from dontmanageerp.setup.install import setup_currency_exchange


def execute():
	dontmanage.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
