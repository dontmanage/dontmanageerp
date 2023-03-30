// Copyright (c) 2018, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

dontmanage.listview_settings['Transaction Deletion Record'] = {
	get_indicator: function(doc) {
		if (doc.docstatus == 0) {
			return [__("Draft"), "red"];
		} else {
			return [__("Completed"), "green"];
		}
	}
};
