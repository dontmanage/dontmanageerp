dontmanage.provide('dontmanageerp.PointOfSale');

dontmanage.pages['point-of-sale'].on_page_load = function(wrapper) {
	dontmanage.ui.make_app_page({
		parent: wrapper,
		title: __('Point of Sale'),
		single_column: true
	});

	dontmanage.require('point-of-sale.bundle.js', function() {
		wrapper.pos = new dontmanageerp.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

dontmanage.pages['point-of-sale'].refresh = function(wrapper) {
	if (document.scannerDetectionData) {
		onScan.detachFrom(document);
		wrapper.pos.wrapper.html("");
		wrapper.pos.check_opening_entry();
	}
};
