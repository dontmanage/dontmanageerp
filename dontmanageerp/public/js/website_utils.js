// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

if(!window.dontmanageerp) window.dontmanageerp = {};

dontmanageerp.subscribe_to_newsletter = function(opts, btn) {
	return dontmanage.call({
		type: "POST",
		method: "dontmanage.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: {"email": opts.email},
		callback: opts.callback
	});
}
