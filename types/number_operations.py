# this enables gapprox to perform operations between numbers

from dataclasses import dataclass

def _check_type(arg0, *args):
	"verify if args are an instance of Number. then check their homogeneity (all are same type)"
	arg0_type = type(arg0)
	for arg in (arg0, *args):
		if not isinstance(arg, Number):
			raise TypeError(f"{arg} should be a Number, not {type(arg)}")
		if type(arg) != arg0_type:
			raise TypeError(f"arguments are of different number types")

@dataclass
class CoercionPolicy:
	implicit_demotion:bool = False
	implicit_promotion:bool = False
	explicit_demotion:bool = False
	explicit_promotion:bool = False

DEFAULT_POLICY = CoercionPolicy()

# built-in binary Number to Number operators -------------------------

def addition(a, b, coercion_policy:CoercionPolicy=DEFAULT_POLICY):
	"a + b"
	_check_type(a, b)

	if isinstance(a, Natural):
		return Natural(a.value+b.value)
	elif isinstance(a, Whole):
		return Whole(a.value+b.value)
	elif isinstance(a, Integer):
		return Integer(a.value+b.value)
	elif isinstance(a, Rational):
		return Rational(a.value+b.value)
	elif isinstance(a, Real):
		return Real(a.value+b.value)
	elif isinstance(a, Complex):
		return Complex(a.real+b.real, a.imaginary+b.imaginary)
	else:
		raise ValueError(f"addition does not support {type(a)}")

def subtraction(a, b, coercion_policy:CoercionPolicy=DEFAULT_POLICY):
	"a - b"
	_check_type(a, b)

	if isinstance(a, Natural):
		return Natural(a.value-b.value)
	elif isinstance(a, Whole):
		return Whole(a.value-b.value)
	elif isinstance(a, Integer):
		return Integer(a.value-b.value)
	elif isinstance(a, Rational):
		return Rational(a.value-b.value)
	elif isinstance(a, Real):
		return Real(a.value-b.value)
	elif isinstance(a, Complex):
		return Complex(a.real-b.real, a.imaginary-b.imaginary)
	else:
		raise ValueError(f"subtraction does not support {type(a)}")

def multiplication(a, b, coercion_policy:CoercionPolicy=DEFAULT_POLICY):
	"a * b"
	_check_type(a, b)

def division(a, b):
	"a / b"
	_check_type(a, b)

def division_remainder(a, b):
	"a % b"
	_check_type(a, b)

def division_quotient(a, b):
	"a // b"
	_check_type(a, b)

def exponentiation(a, b):
	"a ** b"
	_check_type(a, b)

# binary Number to Truth operators ------------------------------

def equal_to(a, b):
	"a == b"
	_check_type(a, b)
	
def not_equal_to(a, b):
	"a != b"
	_check_type(a, b)

def less_than(a, b):
	"a < b"
	_check_type(a, b)

def less_than_or_equal_to(a, b):
	"a <= b"
	_check_type(a, b)

def greater_than(a, b):
	"a > b"
	_check_type(a, b)

def greater_than_or_equal_to(a, b):
	"a >= b"
	_check_type(a, b)

# unary operators ----------------------------------

def absolute(a):
	_check_type(a)

def positive(a):
	_check_type(a)

def negative(a):
	_check_type(a)

def modulus(a):
	_check_type(a)

def floor(a):
	_check_type(a)

def ceiling(a):
	_check_type(a)

def round(a):
	_check_type(a)

# ternary operators -------------------------------

#def hyperoperation(a, b, n):
	
# 

# miscellaneous -----------------------------------

"""
def or

def int
def float
def str
def bool
"""
