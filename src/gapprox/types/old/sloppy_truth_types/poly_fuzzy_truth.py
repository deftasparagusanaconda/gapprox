from .truth_types import CompositeTruth
from .fuzzy_truth import FuzzyTruth

class PolyFuzzyTruth(CompositeTruth):
	"a Truth representing an ordered collection of FuzzyTruth"
	def __init__(self, arg1, *args):
		if hasattr(arg1, '__iter__') and len(args)==0:
			if not all(isinstance(value, FuzzyTruth) for value in arg1):
				raise TypeError(f"expected {arg1} to have only FuzzyTruth")
			self.values = tuple(arg1)
		elif all(isinstance(value, FuzzyTruth) for value in (arg1, args)):
			self.values = tuple((arg1, *args))
		else:
			raise TypeError("expected one iterable of FuzzyTruth or multiple FuzzyTruth")
	"""
	def __lt__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a<b for a,b in zip(self.values, other.values))

	def __le__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a<=b for a,b in zip(self.values, other.values))

	def __eq__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a==b for a,b in zip(self.values, other.values))

	def __ne__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a!=b for a,b in zip(self.values, other.values))

	def __ge__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a>=b for a,b in zip(self.values, other.values))

	def __gt__(self, other):
		if not isinstance(other, PolyFuzzyTruth):
			return NotImplemented
		elif len(self.values) != len(other.values):
			return ValueError("mismatched PolyFuzzyTruth lengths")
		else:
			return PolyBoolean(a>b for a,b in zip(self, other))
	"""
	def __iter__(self):    # could also return self.values directly
		return iter(self.values)

	def __len__(self):
		return len(self.value)

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
		return f"<gapprox.PolyFuzzyTruth{self.values!r}>"

	def __hash__(self):
		return hash(self.values)
