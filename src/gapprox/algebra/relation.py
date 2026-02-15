from .domain import Domain
from typing import Any
from collections.abc import Container, Sequence

class Relation:
	"""represents a mathematical relation. it stores a set of tuples in .tuples and also keeps track of a tuple of domains in .domains. it thus generalizes to an n-ary relation. it can also store tuples as a callable, which is the indicator function of the set"""

	def __init__(self, tuples: Container[Sequence[Any, ...]], domains: Sequence[Domain, ...]):
		if not isinstance(tuples, Container):
			raise AttributeError(f'{tuples} doesnt have __contains__. i recommend using Domain, instead of set or list or something')
		self.tuples: Container[Sequence[Any, ...]] = tuples
		self.domains: Sequence[Domain, ...] = domains
	
	def relates(tuple: Sequence[Any, ...]) -> bool:	
		# yes i do realize im shadowing the python tuple keyword. THIS IS FINE CALM DOWN
		return tuple in self.tuples
	
	__contains__ = relates
