import dontmanage


def get_context(context):
	context.no_cache = 1

	task = dontmanage.get_doc("Task", dontmanage.form_dict.task)

	context.comments = dontmanage.get_all(
		"Communication",
		filters={"reference_name": task.name, "comment_type": "comment"},
		fields=["subject", "sender_full_name", "communication_date"],
	)

	context.doc = task
