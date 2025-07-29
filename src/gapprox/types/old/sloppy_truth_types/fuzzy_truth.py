from .truth_types import AtomicTruth

class FuzzyTruth(AtomicTruth):
	"a fuzzy truth value denoting something between or beyond False/True"
	def __init__(self, value):
		self.value = value
	"""
	def __lt__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, FuzzyTruth):
			return NotImplemented
		return Boolean(self.value > other.value)
	"""
	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.FuzzyTruth({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

