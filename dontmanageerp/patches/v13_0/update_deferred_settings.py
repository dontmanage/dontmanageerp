# Copyright (c) 2019, DontManage and Contributors
# License: GNU General Public License v3. See license.txt

import dontmanage


def execute():
	accounts_settings = dontmanage.get_doc("Accounts Settings", "Accounts Settings")
	accounts_settings.book_deferred_entries_based_on = "Days"
	accounts_settings.book_deferred_entries_via_journal_entry = 0
	accounts_settings.submit_journal_entries = 0
	accounts_settings.save()
