from abc import ABC

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
		self.value = value

class Whole(ScalarNumber):
	"0, 1, 2, 3, ..."
	def __init__(self, value):
		if value < 0:
			raise ValueError(f"{value} is <0")
		self.value = value

class Integer(ScalarNumber):
	"0, -1, 1, -2, 2, -3, 3, ..."
	def __init__(self, value):
		self.value = value

class Rational(ScalarNumber):
	"a Number that can be represented by a division of two Integers, where the denominator is not zero"
	def __init__(self, value):
		self.value = value

class Irrational(ScalarNumber):
	"a Number that cannot be represented by a division of two Integers"
	def __init__(self, value):
		self.value = value

class Real(ScalarNumber):
	"a Number that can be either Rational or Irrational"
	def __init__(self, value):
		self.value = value

class Imaginary(CompositeNumber):
	"a Number multiplied with i such that i**2 = -1"
	def __init__(self, value:ScalarNumber):
		self.value = value

class Complex(Hypercomplex):
	"a + bi where a and b are Real and i² is -1"
	def __init__(self, value1, value2):
		if isinstance(value1, ScalarNumber) and isinstance(value2, ScalarNumber):
			self.value1 = value1
			self.value2 = value2

		elif isinstance(value1, ScalarNumber) and isinstance(value2, Imaginary):
			self.value1 = value1
			self.value2 = value2.value

		else:
			raise ValueError("expected two ScalarNumber or a ScalarNumber and an Imaginary")

class Dual(Hypercomplex):
	"a + bε where a and b are Real and ε² = 0 but ε != 0"
	def __init__(self, value1:ScalarNumber, value2:ScalarNumber):
		self.value1 = value1
		self.value2 = value2

class SplitComplex(Hypercomplex):
	"a + bj where a and b are Real and j² = 1 but j != 1"
	def __init__(self, value1:ScalarNumber, value2:ScalarNumber):
		self.value1 = value1
		self.value2 = value2

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
			raise ValueError("expected four ScalarNumber or two Complex")

class Octonion(Hypercomplex):
	"a + bi + cj + dk + el + fm + gn + ho where a,b,c,d,e,f,g,h are Real and oh just look up the multiplication table its a whole value sorry"
	def __init__(self, a1, a2, a3, a4, a5, a6, a7, a8):
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
			raise ValueError("expected eight ScalarNumber or four Complex or two Quaternion")
