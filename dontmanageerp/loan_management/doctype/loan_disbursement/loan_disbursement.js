// Copyright (c) 2019, DontManage and contributors
// For license information, please see license.txt

{% include 'dontmanageerp/loan_management/loan_common.js' %};

dontmanage.ui.form.on('Loan Disbursement', {
	refresh: function(frm) {
		frm.set_query('against_loan', function() {
			return {
				'filters': {
					'docstatus': 1,
					'status': 'Sanctioned'
				}
			}
		})
	}
});
