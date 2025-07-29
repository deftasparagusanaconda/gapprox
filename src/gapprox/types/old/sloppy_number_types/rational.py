from .number_types import ScalarNumber
from ..truth_types.boolean import Boolean

class Rational(ScalarNumber):
	"a Number that can be represented by a division of two Integers, where the denominator is not zero"
	def __init__(self, value):
		self.value = value

	def __abs__(self):
		return Rational(abs(self.value))

	def __pos__(self):
		return self

	def __neg__(self):
		return Rational(-self.value)

	def __add__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Rational(self.value + other.value)

	def __mul__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Rational(self.value * other.value)

	def __lt__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Rational):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Rational({self.value!r})>"

	def __hash__(self):
		return hash(self.value)
