from .relations import Domain as _Domain
import math as _math
import numbers as _numbers

def _is_in_numbers(number) -> bool:
	return isinstance(number, _numbers.Number)

def _is_in_complexes(number) -> bool:
	return isinstance(number, _numbers.Complex)

def _is_in_extended_reals(number) -> bool:
	return isinstance(number, _numbers.Real) and not _math.isnan(number)

def _is_in_reals(number) -> bool:
	return isinstance(number, _numbers.Real) and _math.isfinite(number)

def _is_in_rationals(number) -> bool:
	return isinstance(number, _numbers.Rational)

def _is_in_integers(number) -> bool:
	return isinstance(number, _numbers.Integral)

numbers        = _Domain(_is_in_numbers)
complexes      = _Domain(_is_in_complexes)
extended_reals = _Domain(_is_in_extended_reals)
reals          = _Domain(_is_in_reals)
rationals      = _Domain(_is_in_rationals)
integers       = _Domain(_is_in_integers)

