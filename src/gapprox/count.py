from typing import Iterable

def count(stuff:Iterable, *, include:set|Iterable=None, exclude:set|Iterable=None):
	'count how many things are in stuff, either including or excluding a set of things'

	if include is not None and exclude is not None:
		raise ValueError("specify either include or exclude only")
	elif include is not None:
		return sum(thing in include for thing in stuff)
	elif exclude is not None:
		return sum(thing not in exclude for thing in stuff)
	else:
		return len(stuff)
