from collections.abc import Callable
from typing import Any

class Mapping:
	"represents a unidirectional mapping from a domain to a codomain. mathematically, a mapping is an looser term than a function because it doesnt need to know the domain or codomain. here it is simply anything that can map a value to another (implements __getitem__) or a function that can return a value given some value (implements __call__)"

	def __init__(self, mapper):
		if not callable(mapper) and not hasattr(mapper, '__getitem__'):
			raise ValueError("invalid mapper type. the mapper must implement either __getitem__ or __call__")
		self.mapper = mapper
	
	def maps_to(self, thing: Any) -> Any: 
		if hasattr(self.mapper, '__getitem__'):
			return self.mapper[thing]
		elif callable(self.mapper):	# has __call__
			return self.mapper(thing)
		else:
			raise ValueError(f"unsupported mapper {self.mapper!r} of type {type(self.mapper)}")
	
	__call__ = maps_to
