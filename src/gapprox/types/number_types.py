from abc import ABC
from .truth_types import Boolean, PolyBoolean

class Number(ABC):
	"an object representing a quantity or an idea of such"
	...

class ScalarNumber(Number):
	"a Number which lives on the one-dimensional real number line"
	...

class CompositeNumber(Number):
	"a Number which is composed of ScalarNumber, like a Number compound"
	...

class Hypercomplex(CompositeNumber):
	"a number that does not live on just the real number line and often has more than one scalar dimension and with special algebraic rules like imaginary units, nilpotent elements, noncommutativity, etc."
	...

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

	def __abs__(self):
		return self

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

class Whole(ScalarNumber):
	"0, 1, 2, 3, ..."
	def __init__(self, value):
		if value < 0:
			raise ValueError(f"{value} is <0")
		if int(value) != value:
			raise ValueError(f"{value} has fractional component")
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Whole):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __abs__(self):
		return self

	def __int__(self):
		return int(self.value)

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Whole({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

class Integer(ScalarNumber):
	"0, -1, 1, -2, 2, -3, 3, ..."
	def __init__(self, value):
		if int(value) != value:
			raise ValueError(f"{value} has fractional component")
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Integer):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __abs__(self):
		return Integer(abs(self.value))

	def __int__(self):
		return int(self.value)

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Integer({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

class Rational(ScalarNumber):
	"a Number that can be represented by a division of two Integers, where the denominator is not zero"
	def __init__(self, value):
		self.value = value

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

	def __abs__(self):
		return Rational(abs(self.value))

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

class Irrational(ScalarNumber):
	"a Number that cannot be represented by a division of two Integers"
	def __init__(self, value):
		self.value = value

	def __lt__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value < other.value)

	def __le__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value <= other.value)

	def __eq__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value != other.value)

	def __ge__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value >= other.value)

	def __gt__(self, other):
		if not isinstance(other, Irrational):
			return NotImplemented
		return Boolean(self.value > other.value)

	def __abs__(self):
		return Irrational(abs(self.value))

	def __float__(self):
		return float(self.value)

	def __complex__(self):
		return complex(self.value)

	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return f"<gapprox.Irrational({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

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

	def __abs__(self):
		return Real(abs(self.value))

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

	def __complex__(self):
		return complex(0, float(self.value))

	def __str__(self):
		return f"{self.value}i"
	
	def __repr__(self):
		return f"<gapprox.Imaginary({self.value!r})>"

	def __hash__(self):
		return hash(self.value)

class Complex(Hypercomplex):
	"a + bi where a and b are Real and i² is -1"
	def __init__(self, arg1, arg2):
		if isinstance(arg1, ScalarNumber) and isinstance(arg2, ScalarNumber):
			self.value1 = arg1
			self.value2 = arg2

		elif isinstance(arg1, ScalarNumber) and isinstance(arg2, Imaginary):
			self.value1 = arg1
			self.value2 = arg2.value

		elif isinstance(arg1, Imaginary) and isinstance(arg2, ScalarNumber):
			self.value1 = arg2
			self.value2 = arg1.value

		else:
			raise TypeError("expected two ScalarNumber or one ScalarNumber and one Imaginary")

	def __lt__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __le__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __eq__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1==other.value1, self.value2==other.value2)

	def __ne__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1!=other.value1, self.value2!=other.value2)

	def __ge__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __gt__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __complex__(self):
		return complex(float(self.value1), float(self.value2))

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}i)"
	
	def __repr__(self):
		return f"<gapprox.Complex({self.value1!r}, {self.value2!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2))

class SplitComplex(Hypercomplex):
	"a + bj where a and b are Real and j² = 1 but j != 1"
	def __init__(self, arg1:ScalarNumber, arg2:ScalarNumber):
		if not (isinstance(arg1, ScalarNumber) and isinstance(arg2, ScalarNumber)):
			raise TypeError("expected two ScalarNumber")
		self.value1 = arg1
		self.value2 = arg2

	def __lt__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __le__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __eq__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1==other.value1, self.value2==other.value2)

	def __ne__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1!=other.value1, self.value2!=other.value2)

	def __ge__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1>=other.value1, self.value2>=other.value2)

	def __gt__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1>other.value1, self.value2>other.value2)

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}j)"
	
	def __repr__(self):
		return f"<gapprox.SplitComplex({self.value1!r}, {self.value2!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2))

class Dual(Hypercomplex):
	"a + bε where a and b are Real and ε² = 0 but ε != 0"
	def __init__(self, arg1:ScalarNumber, arg2:ScalarNumber):
		if not (isinstance(arg1, ScalarNumber) and isinstance(arg2, ScalarNumber)):
			raise TypeError("expected two ScalarNumber")
		self.value1 = arg1
		self.value2 = arg2

	def __lt__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __le__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __eq__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1==other.value1, self.value2==other.value2)

	def __ne__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1!=other.value1, self.value2!=other.value2)

	def __ge__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1>=other.value1, self.value2>=other.value2)

	def __gt__(self, other):
		if not isinstance(other, Dual):
			return NotImplemented
		return PolyBoolean(self.value1>other.value1, self.value2>other.value2)

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}ε)"
	
	def __repr__(self):
		return f"<gapprox.Dual({self.value1!r}, {self.value2!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2))

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

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}i{'' if float(self.value3)<0 else '+'}{self.value3}j{'' if float(self.value4)<0 else '+'}{self.value4}k)"

	def __repr__(self):
		return f"<gapprox.Quaternion({self.value1!r}, {self.value2!r}, {self.value3!r}, {self.value4!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4))

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
		if not isinstance(other, Quaternion):
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
		if not isinstance(other, Quaternion):
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
		if not isinstance(other, Quaternion):
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

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}e1{'' if float(self.value3)<0 else '+'}{self.value3}e2{'' if float(self.value4)<0 else '+'}{self.value4}e3{'' if float(self.value5)<0 else '+'}{self.value5}e4{'' if float(self.value6)<0 else '+'}{self.value6}e5{'' if float(self.value7)<0 else '+'}{self.value7}e6{'' if float(self.value8)<0 else '+'}{self.value8}e7)"

	def __repr__(self):
		return f"<gapprox.Octonion({self.value1!r}, {self.value2!r}, {self.value3!r}, {self.value4!r}, {self.value5!r}, {self.value6!r}, {self.value7!r}, {self.value8!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4))
	def __hash__(self):
		return hash((self.value1, self.value2, self.value3, self.value4, self.value5, self.value6, self.value7, self.value8))
