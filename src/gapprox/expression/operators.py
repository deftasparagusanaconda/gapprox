# allows per-session change of a set of operators
# allows surgical definition of operators
# allows alternate operator definitions (like cmath.sin instead of math.sin)
# allows adding or removing wanted/unwanted operators like adding median, or removing lerp
# allows flexibility of program

import math
import cmath
import operator 
import builtins
import random
import statistics

class OperatorDict(dict):
	'simple wrapper for dict that allows direct dot-notation access. this class was AI-generated lmao. btw, the program wont expect this specific wrapper so feel free to change it out with a normal dict'
	def __getattr__(self, key): return self[key]
	def __setattr__(self, key, value): self[key] = value
	def __delattr__(self, key): del self[key]
	#def __dir__(self): return list(self.keys)

def generalized_mean(data, p):
	'returns the power mean of a list for given p (p=1: arithmetic, 0: geometric, -1: harmonic)'
	n = len(data)
	if p == 0:
		from math import log, exp
		logsum = sum(log(x) for x in data) / n
		return exp(logsum)
	return (sum(x**p for x in data) / n)**(1/p)

def mean(*args):
	'arithmetic mean'
	from statistics import mean
	return mean(args)

def median(*args):
	from statistics import median
	return median(args)

def mode(*args):
	from statistics import mode
	return mode(args)

def reciprocal(x):
	'y such that x*y = 1, where 1 is the multiplicative identity'
	return 1/x

def root(x, base):
	'root of a number in an arbitrary base'
	return x**(1/base)

def fractional_part(x):
	'the non-integer part of a number'
	from math import modf
	return modf(x)[0]

def ifelse(a,b,c): 
	'return b if a is true, otherwise return c'
	return b if a else c

def cot(x):
	'complementary of circular tangent'
	from cmath import tan
	return 1/tan(a)

def sec(x):
	'circular secant'
	from cmath import cos
	return 1/cos(a)

def csc(x):
	'complementary of circular secant'
	from cmath import sin
	return 1/sin(a)

def acot(x):
	'arc length of complementary of circular tangent'
	from cmath import atan
	return atan(1/a)

def asec(x):
	'arc length of circular secant'
	from cmath import acos
	return acos(1/a)

def acsc(x):
	'arc length of complementary of circular secant'
	from cmath import asin
	return asin(1/a)

def coth(x):
	'complementary of hyperbolic tangent'
	from cmath import tanh
	return 1/math.tanh(a)

def sech(x):
	'hyperbolic secant'
	from cmath import cosh
	return 1/math.cosh(a)

def csch(x):
	'complementary of hyperbolic secant'
	from cmath import sinh
	return 1/math.sinh(a)

def acoth(x):
	'arc length of complementary of hyperbolic tangent'
	from cmath import atanh
	return atanh(1/a)

def asech(x):
	'arc length of hyperbolic secant'
	from cmath import acosh
	return acosh(1/a)

def acsch(x):
	'arc length of complementary of hyperbolic secant'
	from cmath import asinh
	return asinh(1/a)

def get_real(x):
	'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
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
	return math.prod(expr(var=value) for value in range(lower, upper))

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

operators = OperatorDict()

# arithmetic
operators.add = operator.add
operators.sub = operator.sub
operators.mul = operator.mul
operators.div = operator.truediv

# numeric
operators.mod   = operator.mod
operators.quot  = operator.floordiv
operators.abs   = operator.abs
operators.neg   = operator.neg
operators.inv   = reciprocal
operators.pow   = operator.pow
operators.floor = math.floor
operators.round = builtins.round
operators.ceil  = math.ceil
operators.ipart = math.trunc
operators.fpart = fractional_part
operators.exp   = math.exp
operators.exp2  = math.exp2
operators.log10 = math.log10
operators.log2  = math.log2
operators.log   = math.log
operators.sqrt  = math.sqrt
operators.cbrt  = math.cbrt
operators.root  = root

# trigonometric
operators.sin   = cmath.sin
operators.cos   = cmath.cos
operators.tan   = cmath.tan
operators.cot   = cot
operators.sec   = sec
operators.csc   = csc
operators.asin  = cmath.asin
operators.acos  = cmath.acos
operators.atan  = cmath.atan
operators.acot  = acot
operators.asec  = asec
operators.acsc  = acsc
operators.sinh  = cmath.sinh
operators.cosh  = cmath.cosh
operators.tanh  = cmath.tanh
operators.coth  = coth
operators.sech  = sech
operators.csch  = csch
operators.asinh = cmath.asinh
operators.acosh = cmath.acosh
operators.atanh = cmath.atanh
operators.acoth = acoth
operators.asech = asech
operators.acsch = acsch

""" left out due to obscurity. also probably mostly wrong :P
operators.versin     = lambda a: 1 - math.cos(a)
operators.coversin   = lambda a: 1 - math.sin(a)
operators.haversin   = lambda a: 0.5 - math.cos(a)/2
operators.hacoversin = lambda a: 0.5 - math.sin(a)/2
operators.exsec      = lambda a: 1/math.cos(a) - 1
operators.excsc      = lambda a: 1/math.sin(a) - 1
operators.chord      = lambda a: 2 * math.sin(a/2)
operators.vercos     = lambda a: 1 + math.cos(a)
operators.covercos   = lambda a: 1 + math.sin(a)
operators.havercos   = lambda a: 0.5 + math.cos(a)/2
operators.hacovercos = lambda a: 0.5 + math.sin(a)/2
"""

# complex
operators.real = get_real
operators.imag = get_imag
operators.arg  = cmath.phase
operators.conj = call_conjugate

# boolean
operators.not_ = operator.not_        # 10
operators.and_ = operator.and_        # 0001
operators.or_  = operator.or_         # 0111
operators.nand = nand                 # 1110
operators.nor  = nor                  # 1000
operators.xor  = operator.xor         # 0110
operators.xnor = operator.eq          # 1001
operators.imp  = implication          # 1101
operators.con  = converse_implication # 1011
operators.nimp = nimp                 # 0010
operators.ncon = ncon                 # 0100

# comparative
operators.lt = operator.lt
operators.le = operator.le
operators.eq = operator.eq
operators.ne = operator.ne
operators.ge = operator.ge
operators.gt = operator.gt

# statistical
operators.mean   = mean
operators.median = median
operators.mode   = mode
operators.pmean  = generalized_mean

# combinatorial
operators.comb = math.comb
operators.perm = math.perm

# miscellaneous
operators.lshift = operator.lshift
operators.rshift = operator.rshift
operators.sign   = signum
operators.ifelse = ifelse
operators.fact   = math.factorial
operators.gamma  = math.gamma
operators.sumt   = sumtorial
operators.gcd    = math.gcd
operators.lcm    = math.lcm
operators.clamp  = clamp
operators.lerp   = lerp
operators.unlerp = unlerp
operators.min    = builtins.min
operators.max    = builtins.max
