# be *veeery* careful how you define these domains. for example, float('inf') does not belong in reals

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

def _is_in_evens(number) -> bool:
	return number % 2 == 0

def _is_in_odds(number) -> bool:
	return number % 2 == 1

def _is_in_primes(number) -> bool:
	raise NotImplementedError

def _is_in_composites(number) -> bool:
	raise NotImplementedError

numbers        = _Domain(_is_in_numbers)
complexes      = _Domain(_is_in_complexes)
extended_reals = _Domain(_is_in_extended_reals)
reals          = _Domain(_is_in_reals)
rationals      = _Domain(_is_in_rationals)
integers       = _Domain(_is_in_integers)
evens          = _Domain(_is_in_evens)
odds           = _Domain(_is_in_odds)
primes         = _Domain(_is_in_primes)
composites     = _Domain(_is_in_composites)

