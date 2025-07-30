import math
import cmath
import operator 
import builtins
import random
import statistics

def multiplicative_inverse(x):
	'y such that x*y = 1, where 1 is the multiplicative identity'
	return 1/x

def root(x, base):
	'root of a number in an arbitrary base'
	return x**(1/base)

def fractional_part(x):
	'the non-integer part of a number'
	from math import modf
	return modf(x)[0]

def cotangent_circular(x):
	'complementary of circular tangent'
	from cmath import tan
	return 1/tan(a)

def secant_circular(x):
	'circular secant'
	from cmath import cos
	return 1/cos(a)

def cosecant_circular(x):
	'complementary of circular secant'
	from cmath import sin
	return 1/sin(a)

def arccotangent_circular(x):
	'arc length of complementary of circular tangent'
	from cmath import atan
	return atan(1/a)

def arcsecant_circular(x):
	'arc length of circular secant'
	from cmath import acos
	return acos(1/a)

def arccosecant_circular(x):
	'arc length of complementary of circular secant'
	from cmath import asin
	return asin(1/a)

def cotangent_hyperbolic(x):
	'complementary of hyperbolic tangent'
	from cmath import tanh
	return 1/math.tanh(a)

def secant_hyperbolic(x):
	'hyperbolic secant'
	from cmath import cosh
	return 1/math.cosh(a)

def cosecant_hyperbolic(x):
	'complementary of hyperbolic secant'
	from cmath import sinh
	return 1/math.sinh(a)

def arccotangent_hyperbolic(x):
	'arc length of complementary of hyperbolic tangent'
	from cmath import atanh
	return atanh(1/a)

def arcsecant_hyperbolic(x):
	'arc length of hyperbolic secant'
	from cmath import acosh
	return acosh(1/a)

def arccosecant_hyperbolic(x):
	'arc length of complementary of hyperbolic secant'
	from cmath import asinh
	return asinh(1/a)

# arithmetic
addition       = operator.add
subtraction    = operator.sub
multiplication = operator.mul
division       = operator.truediv

# numeric
modulus                = operator.mod
quotient               = operator.floordiv
absolute               = operator.abs
additive_inverse       = operator.neg
multiplicative_inverse = multiplicative_inverse
exponentiation         = operator.pow
floor                  = math.floor
round                  = builtins.round
ceiling                = math.ceil
integer_part           = math.trunc
fractional_part        = fractional_part
exponential_base_e     = math.exp
exponential_base_2     = math.exp2
logarithm_base_10      = math.log10
logarithm_base_2       = math.log2
logarithm_base_e       = math.log
square_root            = math.sqrt
cube_root              = math.cbrt
root                   = root

# trigonometric
sine_circular           = math.sin
cosine_circular         = math.cos
tangent_circular        = math.tan
cotangent_circular      = cotangent_circular
secant_circular         = secant_circlar
cosecant_circular       = cosecant_circular
arcsine_circular        = math.asin
arccosine_circular      = math.acos
arctangent_circular     = math.atan
arccotangent_circular   = arccotangent_circular
arcsecant_circular      = arcsecant_circular
arccosecant_circular    = arccosecant_circular
sine_hyperbolic         = math.sinh
cosine_hyperbolic       = math.cosh
tangent_hyperbolic      = math.tanh
cotangent_hyperbolic    = cotangent_hyperbolic
secant_hyperbolic       = secant_hyperbolic
cosecant_hyperbolic     = cosecant_hyperbolic
arcsine_hyperbolic      = math.asinh
arccosine_hyperbolic    = math.acosh
arctangent_hyperbolic   = math.atanh
arccotangent_hyperbolic = arccotangent_hyperbolic
arcsecant_hyperbolic    = arcsecant_hyperbolic
arccosecant_hyperbolic  = arccosecant_hyperbolic

# complex
real_part      = lambda a: a.real
imaginary_part = lambda a: a.imag
argument       = cmath.phase
conjugate      = lambda a: a.conjugate()

# boolean
negation               = operator.not_
conjunction            = operator.and_
disjunction            = operator.or_
implication            = lambda a,b: not a or b
nand                   = lambda a,b: not(a and b)
nor                    = lambda a,b: not(a or b)
exclusive_disjunction  = lambda a,b: a != b
equivalence            = lambda a,b: a == b

# comparative
less_than                = operator.lt
less_than_or_equal_to    = operator.le
equal                    = operator.eq
not_equal                = operator.ne
greater_than_or_equal_to = operator.ge
greater_than             = operator.gt

# logical

# bitwise
bitwise_not = operator.invert
bitwise_and = operator.and_
bitwise_or  = operator.or_
bitwise_xor = operator.xor
bitwise_left_shift = operator.lshift
bitwise_right_shift = operator.rshift

# statistical

# matrix
def determinant(a):
	'unary |mat|'
	raise NotImplementedError

def transpose(a):
	'unary mat\''
	raise NotImplementedError

def dot_product(a, b):
	'binary vector A • vector B'
	raise NotImplementedError

def cross_product(a, b):
	'binary vector A × vector B'
	raise NotImplementedError

# infinitesimal

def limit():
	'quadric (func var, val, direction)'
	raise NotImplementedError

def definite_integral():
	'quadric integral a to b, f(x)dx(func(var, lower, upper))'
	raise NotImplementedError

def indefinite_integral():
	'binary ∫f(x)dx(func, var)'
	raise NotImplementedError

def derivative():
	'binary (func, var)'
	raise NotImplementedError

def partial_derivative():
	'variadic(func, var1, var2, ..., varN)'
	raise NotImplementedError

# miscellaneous
random                       = random.random
signum                       = lambda a: (a>0) - (a<0)
if_then_else                 = lambda cond,yes,no: yes if cond else no
factorial                    = math.factorial
gamma                        = math.gamma
sumtorial                    = lambda a: sum(range(1, a+1))
greatest_common_divisor      = math.gcd    # variadic
lowest_common_multiplier     = math.lcm    # variadic
clamp                        = lambda x,low,high: min(max(x,low),high)
linear_interpolation         = lambda x,low,high: low + x*(high-low)
linear_interpolation_inverse = lambda y,low,high: (y-low)/(high-low)
minimum                      = builtins.min
maximum                      = builtins.max

def piecewise(*args):
	'variadic([cond1, val1], [cond2, val2], ....)'
	raise NotImplementedError

def summation(*args):
	'variadic summation'
	return sum(args)

def product(*args):
	'variadic multiplication'
	return math.prod(args)

def sigma_summation(expr, var, lower, upper):
	'quadric Σ(expr, var, lower, upper)'
	return sum(expr(var=val) for value in range(lower, upper))

def pi_product(expr, var, lower, upper):
	'quadric ∏(expr, var, lower, upper)'
	return math.prod(expr(var=value) for value in range(lower, upper))

#def Modulus():
#	'binary modulus'

#def Quotient(Node):
#	'binary quotient'

# i dont know if modulus and fractional are different
# i also dont know if quotient and floordiv and such are same
