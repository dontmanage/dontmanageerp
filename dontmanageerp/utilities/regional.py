from contextlib import contextmanager

import dontmanage


@contextmanager
def temporary_flag(flag_name, value):
	flags = dontmanage.local.flags
	flags[flag_name] = value
	try:
		yield
	finally:
		flags.pop(flag_name, None)
