from .number_types import ScalarNumber, HyperComplex
from ..truth_types.poly_boolean import PolyBoolean
from .complex import Complex
from .quaternion import Quaternion
from .irrational import Irrational

class Octonion(Hypercomplex):
	"a + bi + cj + dk + el + fm + gn + ho where a,b,c,d,e,f,g,h are Real and oh just look up the multiplication table its a whole thing sorry"
	def __init__(self, a1, a2, a3=None, a4=None, a5=None, a6=None, a7=None, a8=None):
		if isinstance(a1, Quaternion) and isinstance(a2, Quaternion) and all(a is None for a in (a3, a4, a5, a6, a7, a8)):
			self.value1 = a1.value1
			self.value2 = a1.value2
			self.value3 = a1.value3
			self.value4 = a1.value4
			self.value5 = a2.value1
			self.value6 = a2.value2
			self.value7 = a2.value3
			self.value8 = a2.value4

		elif all(isinstance(a, Complex) for a in (a1, a2, a3, a4)) and all(a is None for a in (a5, a6, a7, a8)):
			self.value1 = a1.value1
			self.value2 = a1.value2
			self.value3 = a2.value1
			self.value4 = a2.value2
			self.value5 = a3.value1
			self.value6 = a3.value2
			self.value7 = a4.value1
			self.value8 = a4.value2

		elif all(isinstance(a, ScalarNumber) for a in (a1, a2, a3, a4, a5, a6, a7, a8)):
			self.value1 = a1
			self.value2 = a2
			self.value3 = a3
			self.value4 = a4
			self.value5 = a5
			self.value6 = a6
			self.value7 = a7
			self.value8 = a8

		else:
			raise TypeError("expected eight ScalarNumber or four Complex or two Quaternion")

	def __lt__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 < other.value1, 
			self.value2 < other.value2,
			self.value3 < other.value3, 
			self.value4 < other.value4, 
			self.value5 < other.value5,
			self.value6 < other.value6,
			self.value7 < other.value7, 
			self.value8 < other.value8)

	def __le__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 <= other.value1,
			self.value2 <= other.value2,
			self.value3 <= other.value3,
			self.value4 <= other.value4,
			self.value5 <= other.value5,
			self.value6 <= other.value6,
			self.value7 <= other.value7,
			self.value8 <= other.value8)

	def __eq__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 == other.value1, 
			self.value2 == other.value2,
			self.value3 == other.value3, 
			self.value4 == other.value4, 
			self.value5 == other.value5,
			self.value6 == other.value6,
			self.value7 == other.value7, 
			self.value8 == other.value8)

	def __ne__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 != other.value1,
			self.value2 != other.value2,
			self.value3 != other.value3,
			self.value4 != other.value4,
			self.value5 != other.value5,
			self.value6 != other.value6,
			self.value7 != other.value7,
			self.value8 != other.value8)

	def __ge__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 >= other.value1, 
			self.value2 >= other.value2,
			self.value3 >= other.value3, 
			self.value4 >= other.value4, 
			self.value5 >= other.value5,
			self.value6 >= other.value6,
			self.value7 >= other.value7, 
			self.value8 >= other.value8)

	def __gt__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		return PolyBoolean(
			self.value1 > other.value1,
			self.value2 > other.value2,
			self.value3 > other.value3,
			self.value4 > other.value4,
			self.value5 > other.value5,
			self.value6 > other.value6,
			self.value7 > other.value7,
			self.value8 > other.value8)

	def __add__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		elif any((
			type(self.value1)!=type(other.value1),
			type(self.value2)!=type(other.value2),
			type(self.value3)!=type(other.value3),
			type(self.value4)!=type(other.value4),
			type(self.value5)!=type(other.value5),
			type(self.value6)!=type(other.value6),
			type(self.value7)!=type(other.value7),
			type(self.value8)!=type(other.value8))):
			return NotImplemented
		elif any((
			isinstance(self.value1, Irrational),
			isinstance(self.value2, Irrational),
			isinstance(self.value3, Irrational),
			isinstance(self.value4, Irrational),
			isinstance(self.value5, Irrational),
			isinstance(self.value6, Irrational),
			isinstance(self.value7, Irrational),
			isinstance(self.value8, Irrational))):
			return NotImplemented
		else:
			return Octonion(
				self.value1+other.value1,
				self.value2+other.value2,
				self.value3+other.value3,
				self.value4+other.value4,
				self.value5+other.value5,
				self.value6+other.value6,
				self.value7+other.value7,
				self.value8+other.value8)
			# (a+i)+(b+j)e1+(c+k)e2+(d+l)e3+(e+m)e4+(f+n)e5+(g+o)e6+(h+p)e7
		
	def __mul__(self, other):
		if not isinstance(other, Octonion):
			return NotImplemented
		elif len({type(value) for value in (self.value1, self.value2, self.value3, self.value4, self.value5, self.value6, self.value7, self.value8, other.value1, other.value2, other.value3, other.value4, other.value5, other.value6, other.value7, other.value8)}) != 1:
			return NotImplemented
		elif isinstance(self.value1, Irrational):
			return NotImplemented
		else:
			return Octonion(
				self.value1*other.value1 - self.value2*other.value2 - self.value3*other.value3 - self.value4*other.value4 - self.value5*other.value5 - self.value6*other.value6 - self.value7*other.value7 - self.value8*other.value8,
				self.value1*other.value2 + self.value2*other.value1 + self.value3*other.value4 - self.value4*other.value3 + self.value5*other.value6 - self.value6*other.value5 - self.value7*other.value8 + self.value8*other.value7,
				self.value1*other.value3 - self.value2*other.value4 + self.value3*other.value1 + self.value4*other.value2 + self.value5*other.value7 + self.value6*other.value8 - self.value7*other.value5 - self.value8*other.value6,
				self.value1*other.value4 + self.value2*other.value3 - self.value3*other.value2 + self.value4*other.value1 + self.value5*other.value8 - self.value6*other.value7 + self.value7*other.value6 - self.value8*other.value5,
				self.value1*other.value5 - self.value2*other.value6 - self.value3*other.value7 - self.value4*other.value8 + self.value5*other.value1 + self.value6*other.value2 + self.value7*other.value3 + self.value8*other.value4,
				self.value1*other.value6 + self.value2*other.value5 - self.value3*other.value8 + self.value4*other.value7 - self.value5*other.value2 + self.value6*other.value1 - self.value7*other.value4 + self.value8*other.value3,
				self.value1*other.value7 + self.value2*other.value8 + self.value3*other.value5 - self.value4*other.value6 - self.value5*other.value3 + self.value6*other.value4 + self.value7*other.value1 - self.value8*other.value2,
				self.value1*other.value8 - self.value2*other.value7 + self.value3*other.value6 + self.value4*other.value5 - self.value5*other.value4 - self.value6*other.value3 + self.value7*other.value2 + self.value8*other.value1)
			# hamilton product
		
	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}e1{'' if float(self.value3)<0 else '+'}{self.value3}e2{'' if float(self.value4)<0 else '+'}{self.value4}e3{'' if float(self.value5)<0 else '+'}{self.value5}e4{'' if float(self.value6)<0 else '+'}{self.value6}e5{'' if float(self.value7)<0 else '+'}{self.value7}e6{'' if float(self.value8)<0 else '+'}{self.value8}e7)"

	def __repr__(self):
		return f"<gapprox.Octonion({self.value1!r}, {self.value2!r}, {self.value3!r}, {self.value4!r}, {self.value5!r}, {self.value6!r}, {self.value7!r}, {self.value8!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4))
	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4, self.value5, self.value6, self.value7, self.value8))
