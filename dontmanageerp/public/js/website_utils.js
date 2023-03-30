// Copyright (c) 2015, DontManage and Contributors
// License: GNU General Public License v3. See license.txt

if(!window.dontmanageerp) window.dontmanageerp = {};

// Add / update a new Lead / Communication
// subject, sender, description
dontmanage.send_message = function(opts, btn) {
	return dontmanage.call({
		type: "POST",
		method: "dontmanageerp.templates.utils.send_message",
		btn: btn,
		args: opts,
		callback: opts.callback
	});
};

dontmanageerp.subscribe_to_newsletter = function(opts, btn) {
	return dontmanage.call({
		type: "POST",
		method: "dontmanage.email.doctype.newsletter.newsletter.subscribe",
		btn: btn,
		args: {"email": opts.email},
		callback: opts.callback
	});
}

// for backward compatibility
dontmanageerp.send_message = dontmanage.send_message;
