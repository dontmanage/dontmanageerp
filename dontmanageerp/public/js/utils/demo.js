dontmanage.provide("dontmanageerp.demo");

$(document).on("toolbar_setup", function () {
	if (dontmanage.boot.sysdefaults.demo_company) {
		render_clear_demo_action();
	}
});

function render_clear_demo_action() {
	let demo_action = $(
		`<a class="dropdown-item" onclick="return dontmanageerp.demo.clear_demo()">
			${__("Clear Demo Data")}
		</a>`
	);

	demo_action.appendTo($("#toolbar-user"));
}

dontmanageerp.demo.clear_demo = function () {
	dontmanage.confirm(__("Are you sure you want to clear all demo data?"), () => {
		dontmanage.call({
			method: "dontmanageerp.setup.demo.clear_demo_data",
			freeze: true,
			freeze_message: __("Clearing Demo Data..."),
			callback: function (r) {
				dontmanage.ui.toolbar.clear_cache();
				dontmanage.show_alert({
					message: __("Demo data cleared"),
					indicator: "green",
				});
			},
		});
	});
};
