# this enables gapprox to recognize and preserve number types up to octonions

# number types are a composition of their value type and structure type
# for example, a complex number of natural real and integer imaginary are:
# Complex(Natural, )

from misc import int_to_str
import number_operations

class Number:
	"base class for the number types"
	__add__ = number_operations.addition
	__sub__ = number_operations.subtraction
	__mul__ = number_operations.multiplication
	__truediv__ = number_operations.division
	__divmod__ = number_operations.division_remainder
	__floordiv__ = number_operations.division_quotient
	__pow__ = number_operations.exponentiation

# value ----------------------------------------------------------

class RealBasis(Number):
	"anything that lives on the real number line"

class Natural(RealBasis):
	"1, 2, 3, ..."
	def __init__(self, value):
		if value in number_sets.Naturals:
			self.value:int = int(value)
		else:
			raise ValueError

	def __str__(self):
		return int_to_str(self.value)

	def __repr__(self):
		return "Natural(" + int_to_str(self.value) + ')'
	
class Whole(RealBasis):
	"0, 1, 2, 3, ..."
	def __init__(self, value):
		if value - int(value) != 0 or value < 0:
			raise ValueError
		self.value:int = int(value)
	
	def __str__(self):
		return int_to_str(self.value)
	def __repr__(self):
		return "Natural(" + int_to_str(self.value) + ')'
	
class Integer(RealBasis):
	"0, 1, -1, 2, -2, 3, -3, ..."
	def __init__(self, value):
		if value - int(value) != 0:
			raise ValueError
		self.value:int = int(value)
	
	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return "Integer(" + str(self.value) + ')'
	
class Rational(RealBasis):
	"numbers representable as ratio of integers, given denominator is not zero"
	def __init__(self, arg1, arg2=None):
		if arg2 is None:
			self.value:float = float(value)
		elif arg1 is not None and arg2 is not None:
			self.value:float = arg1/arg2
		else:
			raise ValueError("critical! i dont know what happened!")
	
	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return "Rational(" + str(self.value) + ')'
	
class Irrational(RealBasis):
	def __init__(self, value):
		if not isinstance(value, str):
			raise TypeError("require str input")
		self.value:str = value

	__str__ = lambda : self.value
#	__repr__ = Irrational()

class Real(RealBasis):
	"union of rational and irrational"
	def __init__(self, value):
		if complex(self, value):
			self.value = real
	
	def __str__(self):
		return str(self.value)
	
	def __repr__(self):
		return "Real(" + str(self.value) + ')'
	
# higher dimension numbers------------------------------------------------------
	
# numbers that dont live on the real number line still rely on types that lie on the real number line. for example, gaussian integers rely on Integer, which lives on the real number line. thus, gaussian integers may be modelled as: Complex(Integer(2), Integer(3))

# the hypercomplex hierarchy is done using the Cayley-Dickson construction method where each higher-dimensional number is built from two numbers of lower dimension
		
class Complex(Number):
	"""numbers with real and imaginary components, with i² = -1
can be constructed from 2 RealBasis"""
	def __init__(self, real:RealBasis, imaginary:RealBasis):
		self.real = real
		self.imaginary = imaginary

	def __str__(self):
		return str(self.real) + ' ' + str(self.imaginary)

	def __repr__(self):
		return "Complex(" + str(self.value) + ')'

class HyperComplex(Number):

class Quaternion(Number):
	"""numbers with four components
can be constructed from 4 RealBasis, or 2 Complex"""

class Octonion(Number):
	"""numbers with eight components
can be constructed from 8 RealBasis, 4 Complex, or 2 Quaternion"""
