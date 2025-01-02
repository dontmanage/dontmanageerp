import dontmanage


def get_context(context):
	context.no_cache = 1

	timelog = dontmanage.get_doc("Time Log", dontmanage.form_dict.timelog)

	context.doc = timelog
