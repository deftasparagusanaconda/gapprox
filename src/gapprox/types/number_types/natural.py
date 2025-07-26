from .number_types import ScalarNumber
from ..truth_types.boolean import Boolean

class Natural(ScalarNumber):
	"1, 2, 3, ..."
	def __init__(self, value):
		if value < 1:
			raise ValueError(f"{value} is <1")
		if int(value) != value:
			raise ValueError(f"{value} has fractional component")
		self.value = value
	
	def __lt__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value <= other.value)
	
	def __eq__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value != other.value)
	
	def __ge__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __add__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Natural(self.value + other.value)

	def __mul__(self, other):
		if not isinstance(other, Natural):
			return NotImplemented
		return Natural(self.value * other.value)

#	def __abs__(self):
#		return self

	def __int__(self):
		return int(self.value)

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Natural({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

