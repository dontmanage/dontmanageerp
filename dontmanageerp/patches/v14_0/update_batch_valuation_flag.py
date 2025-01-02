import dontmanage


def execute():
	"""
	- Don't use batchwise valuation for existing batches.
	- Only batches created after this patch shoule use it.
	"""

	batch = dontmanage.qb.DocType("Batch")
	dontmanage.qb.update(batch).set(batch.use_batchwise_valuation, 0).run()
