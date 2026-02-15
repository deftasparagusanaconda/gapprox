# be *veeery* careful how you define these domains. for example, float('inf') does not belong in reals

from .domain import Domain
import math
import numbers

def is_Truth(thing) -> bool:
	return isinstance(thing, bool)

def is_Number(number) -> bool:
	return isinstance(number, numbers.Number)

def is_Complex(number) -> bool:
	return isinstance(number, numbers.Complex)

#def is_Real_and_not_nan(number) -> bool:
#	return isinstance(number, numbers.Real) and not _math.isnan(number)

#def is_Real_and_finite(number) -> bool:
#	return isinstance(number, numbers.Real) and _math.isfinite(number)

def is_Real(number) -> bool:
	return isinstance(number, numbers.Real)

def is_Rational(number) -> bool:
	return isinstance(number, numbers.Rational)

def is_Integral(number) -> bool:
	return isinstance(number, numbers.Integral)

truth    = Domain(is_Truth)
number   = Domain(is_Number)
complex  = Domain(is_Complex)
real     = Domain(is_Real)
rational = Domain(is_Rational)
integral = Domain(is_Integral)

__dir__ = lambda: [
		 'truth'
		,'number'
		,'complex'
		,'real'
		,'rational'
		,'integral'
		]
