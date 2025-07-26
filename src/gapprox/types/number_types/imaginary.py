from .number_types import ScalarNumber, CompositeNumber
from ..truth_types.boolean import Boolean
from .irrational import Irrational

class Imaginary(CompositeNumber):
	"a Number multiplied with i such that i**2 = -1"
	def __init__(self, value:ScalarNumber):
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __add__(self, other):
		if not isinstance(other, Imaginary):
			return NotImplemented
		elif type(self.value) != type(other.value):
			return NotImplemented
		elif isinstance(self.value, Irrational):
			return NotImplemented
		else:
			return Imaginary(self.value + other.value)

	def __complex__(self):
		return complex(0, float(self.value))

	def __str__(self):
		return f"{self.value}i"
	
	def __repr__(self):
		return f"<gapprox.Imaginary({self.value!r})>"

	def __hash__(self):
		return hash(self.value)
