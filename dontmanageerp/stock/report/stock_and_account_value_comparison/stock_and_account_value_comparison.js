// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt


dontmanage.query_reports["Stock and Account Value Comparison"] = {
	"filters": [
		{
			"label": __("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": dontmanage.defaults.get_user_default("Company")
		},
		{
			"label": __("Account"),
			"fieldname": "account",
			"fieldtype": "Link",
			"options": "Account",
			get_query: function() {
				var company = dontmanage.query_report.get_filter_value('company');
				return {
					filters: {
						"account_type": "Stock",
						"company": company
					}
				}
			}
		},
		{
			"label": __("As On Date"),
			"fieldname": "as_on_date",
			"fieldtype": "Date",
			"default": dontmanage.datetime.get_today(),
		},
	],

	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},

	onload(report) {
		report.page.add_inner_button(__("Create Reposting Entries"), function() {
			let message = `<div>
				<p>
					Reposting Entries will change the value of
					accounts Stock In Hand, and Stock Expenses
					in the Trial Balance report and will also change
					the Balance Value in the Stock Balance report.
				</p>
				<p>Are you sure you want to create Reposting Entries?</p>
				</div>
			`;
			let indexes = dontmanage.query_report.datatable.rowmanager.getCheckedRows();
			let selected_rows = indexes.map(i => dontmanage.query_report.data[i]);

			if (!selected_rows.length) {
				dontmanage.throw(__("Please select rows to create Reposting Entries"));
			}

			dontmanage.confirm(__(message), () => {
				dontmanage.call({
					method: "dontmanageerp.stock.report.stock_and_account_value_comparison.stock_and_account_value_comparison.create_reposting_entries",
					args: {
						rows: selected_rows,
						company: dontmanage.query_report.get_filter_values().company
					}
				});

			});
		});
	}
};
