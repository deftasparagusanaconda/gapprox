try:
	from frozendict import frozendict
except ImportError:
	class frozendict(dict):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			# precompute hash based on items
			self._hash = hash(frozenset(self.items()))

		# block all mutation
		def mutating_method(*args, **kwargs):
			raise TypeError("frozendict is immutable")

		__setitem__ = mutating_method
		__delitem__ = mutating_method
		clear = mutating_method
		pop = mutating_method
		popitem = mutating_method
		update = mutating_method
		setdefault = mutating_method
		
		def __hash__(self):
			return self._hash

		def __repr__(self):
			return f"frozendict({dict(self)})"
