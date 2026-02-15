from typing import Any
from collections.abc import Container	# anything that has __contains__
from typing import Callable	# anything that has __call__

class Domain:
	'represents a mathematical domain, which is stored as either a Container[Any] (like a set or a list or a tuple. anything with __contains__ defined), or a Callable[[Any, ...], bool] (like a function or Expression. anything with __call__ defined) which is the indicator function of that set'
	
	def __init__(self, determiner: Container[Any] | Callable[[Any, ...], bool]):
		if not isinstance(determiner, (Container, Callable)):
			raise TypeError(f"{determiner} must be a Container (has __contains__) or a Callable (has __call__)")
		self.determiner = determiner
	
	def has(self, thing: any) -> bool:
		if isinstance(self.determiner, Container):
			return thing in self.determiner
		elif isinstance(self.determiner, Callable):
			return self.determiner(thing)	
		else:
			raise AttributeError("unrecognized determiner")

	__contains__ = has
