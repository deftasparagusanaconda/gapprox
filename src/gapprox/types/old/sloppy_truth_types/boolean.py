from .truth_types import AtomicTruth

class Boolean(AtomicTruth):
	"an AtomicTruth denoting no/yes, false/true, off/on, F/T, 0/1, down/up, open/closed, etc."
	def __init__(self, value):
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __invert__(self):
		return Boolean(not self.value)

	def __and__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value & other.value)

	def __or__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value | other.value)

	def __xor__(self, other):
		if not isinstance(other, Boolean):
			return NotImplemented
		return Boolean(self.value ^ other.value)

	def __bool__(self):
		return bool(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Boolean({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

