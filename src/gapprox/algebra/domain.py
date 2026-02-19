from typing import Any, Type
from collections.abc import Container	# anything that has __contains__
from typing import Callable	# anything that has __call__
import inspect
import numbers

class Domain:
	'represents a mathematical domain, which is stored as either a Container[Any] (like a set or a list or a tuple. anything with __contains__ defined), or a Callable[[Any, ...], bool] (like a function or Expression. anything with __call__ defined) which is the indicator function of that set'
	
	def __init__(self, determiner: Container[Any] | Callable[[Any, ...], bool] | Type):
		if not isinstance(determiner, (Container, Callable)):
			raise TypeError(f"{determiner} must be a Container (has __contains__) or a Callable (has __call__)")
		self.determiner = determiner
	
	def has(self, thing: any) -> bool:
		if isinstance(self.determiner, Container):
			return thing in self.determiner
		elif inspect.isclass(self.determiner):
			return isinstance(thing, self.determiner)
		elif isinstance(self.determiner, Callable):
			return self.determiner(thing)	
		else:
			raise AttributeError("unrecognized determiner")

	__contains__ = has

truth    = Domain(bool)
number   = Domain(numbers.Number)
complex  = Domain(numbers.Complex) 
real     = Domain(numbers.Real) 
rational = Domain(numbers.Rational)
integral = Domain(numbers.Integral)

__dir__ = lambda: [
	'Domain',
	'truth',
	'number',
	'complex',
	'real',
	'rational',
	'integral',
]
