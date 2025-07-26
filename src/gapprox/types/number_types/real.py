from .number_types import ScalarNumber
from ..truth_types.boolean import Boolean

class Real(ScalarNumber):
	"a Number that can be either Rational or Irrational"
	def __init__(self, value):
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __add__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Real(self.value + other.value)

	def __mul__(self, other):
		if not isinstance(other, Real):
			return NotImplemented
		return Real(self.value * other.value)

#	def __abs__(self):
#		return Real(abs(self.value))

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Real({self.value!r})>"

	def __hash__(self):
		return hash(self.value)
