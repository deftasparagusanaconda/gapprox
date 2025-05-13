# this enables gapprox to recognize and preserve number types

# number types are a composition of their value type and structure type
# for example, complex numbers of zero real and integer imaginary are:
# Number(

import number_operations

class Number:
	# abstract class from which number types are derived
	def __init__(self):
		pass

	__add__ = number_operations.addition
	__sub__ = number_operations.subtraction
	__mul__ = number_operations.multiplication
	__truediv__ = number_operations.division
	__divmod__ = number_operations.division_remainder
	__floordiv__ = number_operations.division_quotient
	__pow__ = number_operations.exponentiation

# value ----------------------------------------------------------

class Natural(Number):
	"1, 2, 3, ..."
	def __init__(self, value):
		if value - int(value) != 0 or value < 1:
			raise ValueError
		self.value:int = int(value)
	
	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "Natural(" + str(self.value) + ')'

class Whole(Number):
	"0, 1, 2, 3, ..."
	def __init__(self, value):
		if value - int(value) != 0 or value < 0:
			raise ValueError
		self.value:int = int(value)

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "Whole(" + str(self.value) + ')'

class Integer(Number):
	"0, 1, -1, 2, -2, 3, -3, ..."
	def __init__(self, value):
		if value - int(value) != 0:
			raise ValueError
		self.value:int = int(value)

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "Integer(" + str(self.value) + ')'

class Rational(Number):
	"all numbers representable as ratio of integers, given denominator is not zero"
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

#class Irrational(Number):
#	idk yet

class Real(Number):
	"union of rational and irrational"
	def __init__(self, value):
		if complex(self, value):
			self.value = real

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "Real(" + str(self.value) + ')'

# structure -------------------------------------------------------

class Imaginary(Number):
	"numbers that "

class Complex(Number):
	"complex numbers of the i^2 = -1 variant"
	def __init__(self, real:Real, imaginary:Imaginary):
		self.real = real
		self.imaginary = imaginary

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "Complex(" + str(self.value) + ')'
