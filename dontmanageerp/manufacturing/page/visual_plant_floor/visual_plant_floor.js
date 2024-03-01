

dontmanage.pages['visual-plant-floor'].on_page_load = function(wrapper) {
	var page = dontmanage.ui.make_app_page({
		parent: wrapper,
		title: 'Visual Plant Floor',
		single_column: true
	});

	dontmanage.visual_plant_floor = new dontmanage.ui.VisualPlantFloor(
		{wrapper: $(wrapper).find('.layout-main-section')}, wrapper.page
	);
}