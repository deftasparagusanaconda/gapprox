from .number_types import ScalarNumber, Hypercomplex
from ..truth_types.poly_boolean import PolyBoolean
from .complex import Complex
from .irrational import Irrational

class Quaternion(Hypercomplex):
	"a + bi + cj + dk where a, b, c, d are Real and i² = j² = k² = ijk = 1" # i dont think this fully covers the definition
	def __init__(self, arg1, arg2, arg3=None, arg4=None):
		if all((isinstance(arg1, Complex), isinstance(arg2, Complex), arg3 is None, arg4 is None)):
			self.value1 = arg1.value1
			self.value2 = arg1.value2
			self.value3 = arg2.value1
			self.value4 = arg2.value2

		elif all(isinstance(arg, ScalarNumber) for arg in (arg1, arg2, arg3, arg4)):
			self.value1 = arg1
			self.value2 = arg2
			self.value3 = arg3
			self.value4 = arg4
		else:
			raise TypeError("expected four ScalarNumber or two Complex")

	def __lt__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 < other.value1, 
			self.value2 < other.value2, 
			self.value3 < other.value3, 
			self.value4 < other.value4)

	def __le__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 <= other.value1,
			self.value2 <= other.value2,
			self.value3 <= other.value3,
			self.value4 <= other.value4)

	def __eq__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 == other.value1, 
			self.value2 == other.value2, 
			self.value3 == other.value3, 
			self.value4 == other.value4)

	def __ne__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 != other.value1,
			self.value2 != other.value2,
			self.value3 != other.value3,
			self.value4 != other.value4)

	def __ge__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 >= other.value1, 
			self.value2 >= other.value2, 
			self.value3 >= other.value3, 
			self.value4 >= other.value4)

	def __gt__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		return PolyBoolean(
			self.value1 > other.value1,
			self.value2 > other.value2,
			self.value3 > other.value3,
			self.value4 > other.value4)

	def __add__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		elif type(self.value1)!=type(other.value1) or type(self.value2)!=type(other.value2) or type(self.value3)!=type(other.value3) or type(self.value4)!=type(other.value4):
			return NotImplemented
		elif isinstance(self.value1, Irrational) or isinstance(self.value2, Irrational) or isinstance (self.value3, Irrational) or isinstance(self.value4, Irrational):
			return NotImplemented
		else:
			return Quaternion(self.value1+other.value1, self.value2+other.value2, self.value3+other.value3, self.value4+other.value4)
			# (a+e)+(b+f)i+(c+g)j+(d+h)k
	
	def __mul__(self, other):
		if not isinstance(other, Quaternion):
			return NotImplemented
		elif len({type(value) for value in (self.value1, self.value2, self.value3, self.value4, other.value1, other.value2, other.value3, other.value4)}) != 1:
			return NotImplemented
		elif isinstance(self.value1, Irrational):
			return NotImplemented
		else:
			return Quaternion(
				self.value1*other.value1 - self.value2*other.value2 - self.value3*other.value3 - self.value4*other.value4,
				self.value1*other.value2 + self.value2*other.value1 + self.value3*other.value4 - self.value4*other.value3,
				self.value1*other.value3 - self.value2*other.value4 + self.value3*other.value1 + self.value4*other.value2,
				self.value1*other.value4 + self.value2*other.value3 - self.value3*other.value2 + self.value4*other.value1)
			# hamilton product
		
	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}i{'' if float(self.value3)<0 else '+'}{self.value3}j{'' if float(self.value4)<0 else '+'}{self.value4}k)"
	
	def __repr__(self):
		return f"<gapprox.Quaternion({self.value1!r}, {self.value2!r}, {self.value3!r}, {self.value4!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4))
