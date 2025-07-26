from .truth_types import CompositeTruth
from .boolean import Boolean

class PolyBoolean(CompositeTruth):
	"a Truth representing an ordered collection of Boolean"
	def __init__(self, *args):
		if not all(isinstance(value, Boolean) for value in args):
			raise TypeError("expected Boolean as arguments")
		self.values:tuple = args
	
	def __lt__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a<b for a,b in zip(self, other)))

	def __le__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a<=b for a,b in zip(self, other)))

	def __eq__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a==b for a,b in zip(self, other)))

	def __ne__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a!=b for a,b in zip(self, other)))

	def __ge__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a>=b for a,b in zip(self, other)))

	def __gt__(self, other):
		if not isinstance(other, PolyBoolean):
			return NotImplemented
		if len(self) != len(other):
			return ValueError("mismatched PolyBoolean lengths")
		return PolyBoolean(*(a>b for a,b in zip(self, other)))

	def __iter__(self):    # could also return self.values directly
		return iter(self.values)

	def __len__(self):
		return len(self.values)

	def __getitem__(self, index):
		return self.values[index]

#	def __contains__(self, thing):
#		match_count = sum(1 for value in self.values if value==thing)
#		total = len(self.values)
#		return FuzzyTruth(match_count/total)

	def __contains__(self, value):
		return value in self.values

	def __reversed(self):
		return reversed(self.values)

	def __str__(self):
		return str(self.values)
	
	def __repr__(self):
		return f"<gapprox.PolyBoolean{self.values!r}>"

	def __hash__(self):
		return hash(self.values)

