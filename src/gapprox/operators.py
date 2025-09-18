import math as _math
#import cmath as _cmath
#import operator as _operator
#import numbers as _numbers
#import builtins as _builtins
#import statistics as _statistics

def to_tuple(*args):
	return tuple(args)

def to_list(*args):
	return list(args)

def to_dict(*args):
	return dict(args)

def to_set(*args):
	return set(args)

def generalized_mean(p, *args):
	'returns the power mean for given p (first argument) (p=1: arithmetic, 0: geometric, -1: harmonic)'
	if p == 0:
		return _math.exp(sum(_math.log(x) for x in args)/len(args))
	return (sum(x**p for x in args)/len(args)) ** (1/p)

def mean(*args):
	'arithmetic mean'
	return _statistics.mean(args)

def median(*args):
	return _statistics.median(args)

def mode(*args):
	return _statistics.mode(args)

def reciprocal(x):
	'y such that x*y = 1, where 1 is the multiplicative identity'
	return 1/x

def root(x, base):
	'root of a number in an arbitrary base'
	return x**(1/base)

def square(x):
	'x**2, x*x, x^2, x²'
	return x**2

def cube(x):
	'x**3, x*x*x, x^2, x³'
	return x**3

def fractional_part(x):
	'the non-integer part of a number'
	return _math.modf(x)[0]

def ifelse(a,b,c):
	'return a if b is true, otherwise return c'
	return a if b else c

def cot(x):
	'trigonometric cotangent'
	return 1/_math.tan(x)

def sec(x):
	'trigonometric secant'
	return 1/_math.cos(x)

def csc(x):
	'trigonometric cosecant'
	return 1/_math.sin(x)

def acot(x):
	'inverse trigonometric cotangent'
	return _math.atan(1/x)

def asec(x):
	'inverse trigonometric secant'
	return _math.acos(1/x)

def acsc(x):
	'inverse trigonometric cosecant'
	return _math.asin(1/x)

def coth(x):
	'hyperbolic cotangent'
	return 1/_math.tanh(x)

def sech(x):
	'hyperbolic secant'
	return 1/_math.cosh(x)

def csch(x):
	'hyperbolic cosecant'
	return 1/_math.sinh(x)

def acoth(x):
	'inverse hyperbolic cotangent'
	return _math.atanh(1/x)

def asech(x):
	'inverse hyperbolic secant'
	return _math.acosh(1/x)

def acsch(x):
	'inverse hyperbolic cosecant'
	return _math.asinh(1/x)

def get_real(x):
	'get real lmao https://www.youtube.com/watch?v=dQw4w9WgXcQ'
	return x.real

def get_imag(x):
	'any good complex type should have .real and .imag, right??'
	return x.imag

def call_conjugate(x):
	'returns x.conjugate()'
	return x.conjugate()

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
	return _math.prod(expr(var=value) for value in range(lower, upper))

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

def clamp(x, low, high):
	'return x but constrained within [low, high]'
	return min(max(x,low),high)

def lerp(x, low, high):
	'linear interpolation. allows 1<x<0'
	return low + x*(high-low)

def unlerp(x, low, high):
	'inverse of linear interpolation. allows high<x<low'
	return (x-low)/(high-low)

def sumtorial(x):
	'return sum of all numbers from 1 to x. like factorial but with addition'
	return sum(range(1, a+1))

def signum(a):
	'return -1 if negative, 0 if zero, 1 if positive'
	return (a>0) - (a<0)

def nand(a,b):
	'return not(a and b) AKA ¬(a∧b) AKA negation(conjunction(a,b))'
	return not(a and b)

def nor(a, b):
	'return not(a or b) AKA ¬(a∨b) AKA negation(disjunction(a,b))'
	return not(a or b)

def implication(a, b):
	'return not a or b AKA a->b AKA ¬a∨b AKA disjunction(negation(a),b)'
	return not a or b

def converse_implication(a, b):
	'return a or not b AKA b->a AKA a∨¬b AKA disjunction(a,negation,b)'
	return a or not b

def nimp(a, b):
	'return a and not b AKA ¬(a->b) AKA a∧¬b AKA negation(implication(a,b))'
	return a and not b

def ncon(a, b):
	'return not a and b AKA ¬(a->b) AKA ¬a∧b AKA negation(converse_implication(a,b))'
	return not a and b

def cot_cmath(x):
	'trigonometric cotangent (using cmath)'
	return 1/_cmath.tan(x)

def sec_cmath(x):
	'trigonometric secant (using cmath)'
	return 1/_cmath.cos(x)

def csc_cmath(x):
	'trigonometric cosecant (using cmath)'
	return 1/_cmath.sin(x)

def acot_cmath(x):
	'inverse trigonometric cotangent (using cmath)'
	return _cmath.atan(1/x)

def asec_cmath(x):
	'inverse trigonometric secant (using cmath)'
	return _cmath.acos(1/x)

def acsc_cmath(x):
	'inverse trigonometric cosecant (using cmath)'
	return _cmath.asin(1/x)

def coth_cmath(x):
	'hyperbolic cotangent (using cmath)'
	return 1/_cmath.tanh(x)

def sech_cmath(x):
	'hyperbolic secant (using cmath)'
	return 1/_cmath.cosh(x)

def csch_cmath(x):
	'hyperbolic cosecant (using cmath)'
	return 1/_cmath.sinh(x)

def acoth_cmath(x):
	'inverse hyperbolic cotangent (using cmath)'
	return _cmath.atanh(1/x)

def asech_cmath(x):
	'inverse hyperbolic secant (using cmath)'
	return _cmath.acosh(1/x)

def acsch_cmath(x):
	'inverse hyperbolic cosecant (using cmath)'
	return _cmath.asinh(1/x)

def dist(*args):
	'euclidean distance in n dimensions'
	from math import sqrt
	return sqrt(sum(arg**2 for arg in args))
