# "why is there a '_' everywhere?!?"
# because this file is directly exposed in the module's namespace, and we want only the operator_dicts to be visible; not anything else

#from .miscellaneous.dot_dict import DotDict as _DotDict
import math as _math
import cmath as _cmath
import operator as _operator
import numbers as _numbers
import builtins as _builtins
import statistics as _statistics

def _to_tuple(*args):
	return tuple(args)

def _to_list(*args):
	return list(args)

def _to_dict(*args):
	return dict(args)

def _to_set(*args):
	return set(args)

def _generalized_mean(p, *args):
	'returns the power mean for given p (first argument) (p=1: arithmetic, 0: geometric, -1: harmonic)'
	if p == 0:
		return _math.exp(sum(_math.log(x) for x in args)/len(args))
	return (sum(x**p for x in args)/len(args)) ** (1/p)

def _mean(*args):
	'arithmetic mean'
	return _statistics.mean(args)

def _median(*args):
	return _statistics.median(args)

def _mode(*args):
	return _statistics.mode(args)

def _reciprocal(x):
	'y such that x*y = 1, where 1 is the multiplicative identity'
	return 1/x

def _root(x, base):
	'root of a number in an arbitrary base'
	return x**(1/base)

def _square(x):
	'x**2, x*x, x^2, x²'
	return x**2

def _cube(x):
	'x**3, x*x*x, x^2, x³'
	return x**3

def _fractional_part(x):
	'the non-integer part of a number'
	return _math.modf(x)[0]

def _ifelse(a,b,c):
	'return a if b is true, otherwise return c'
	return a if b else c

def _cot(x):
	'trigonometric cotangent'
	return 1/_math.tan(x)

def _sec(x):
	'trigonometric secant'
	return 1/_math.cos(x)

def _csc(x):
	'trigonometric cosecant'
	return 1/_math.sin(x)

def _acot(x):
	'inverse trigonometric cotangent'
	return _math.atan(1/x)

def _asec(x):
	'inverse trigonometric secant'
	return _math.acos(1/x)

def _acsc(x):
	'inverse trigonometric cosecant'
	return _math.asin(1/x)

def _coth(x):
	'hyperbolic cotangent'
	return 1/_math.tanh(x)

def _sech(x):
	'hyperbolic secant'
	return 1/_math.cosh(x)

def _csch(x):
	'hyperbolic cosecant'
	return 1/_math.sinh(x)

def _acoth(x):
	'inverse hyperbolic cotangent'
	return _math.atanh(1/x)

def _asech(x):
	'inverse hyperbolic secant'
	return _math.acosh(1/x)

def _acsch(x):
	'inverse hyperbolic cosecant'
	return _math.asinh(1/x)

def _get_real(x):
	'get real lmao https://www.youtube.com/watch?v=dQw4w9WgXcQ'
	return x.real

def _get_imag(x):
	'any good complex type should have .real and .imag, right??'
	return x.imag

def _call_conjugate(x):
	'returns x.conjugate()'
	return x.conjugate()

def _piecewise(*args):
	'variadic([cond1, val1], [cond2, val2], ....)'
	raise NotImplementedError

def _summation(*args):
	'variadic summation'
	return sum(args)

def _product(*args):
	'variadic multiplication'
	return math.prod(args)

def _sigma_summation(expr, var, lower, upper):
	'quadric Σ(expr, var, lower, upper)'
	return sum(expr(var=val) for value in range(lower, upper))

def _pi_product(expr, var, lower, upper):
	'quadric ∏(expr, var, lower, upper)'
	return _math.prod(expr(var=value) for value in range(lower, upper))

# matrix
def _determinant(a):
	'unary |mat|'
	raise NotImplementedError

def _transpose(a):
	'unary mat\''
	raise NotImplementedError

def _dot_product(a, b):
	'binary vector A • vector B'
	raise NotImplementedError

def _cross_product(a, b):
	'binary vector A × vector B'
	raise NotImplementedError

# infinitesimal
def _limit():
	'quadric (func var, val, direction)'
	raise NotImplementedError

def _definite_integral():
	'quadric integral a to b, f(x)dx(func(var, lower, upper))'
	raise NotImplementedError

def _indefinite_integral():
	'binary ∫f(x)dx(func, var)'
	raise NotImplementedError

def _derivative():
	'binary (func, var)'
	raise NotImplementedError

def _partial_derivative():
	'variadic(func, var1, var2, ..., varN)'
	raise NotImplementedError

def _clamp(x, low, high):
	'return x but constrained within [low, high]'
	return min(max(x,low),high)

def _lerp(x, low, high):
	'linear interpolation. allows 1<x<0'
	return low + x*(high-low)

def _unlerp(x, low, high):
	'inverse of linear interpolation. allows high<x<low'
	return (x-low)/(high-low)

def _sumtorial(x):
	'return sum of all numbers from 1 to x. like factorial but with addition'
	return sum(range(1, a+1))

def _signum(a):
	'return -1 if negative, 0 if zero, 1 if positive'
	return (a>0) - (a<0)

def _nand(a,b):
	'return not(a and b) AKA ¬(a∧b) AKA negation(conjunction(a,b))'
	return not(a and b)

def _nor(a, b):
	'return not(a or b) AKA ¬(a∨b) AKA negation(disjunction(a,b))'
	return not(a or b)

def _implication(a, b):
	'return not a or b AKA a->b AKA ¬a∨b AKA disjunction(negation(a),b)'
	return not a or b

def _converse_implication(a, b):
	'return a or not b AKA b->a AKA a∨¬b AKA disjunction(a,negation,b)'
	return a or not b

def _nimp(a, b):
	'return a and not b AKA ¬(a->b) AKA a∧¬b AKA negation(implication(a,b))'
	return a and not b

def _ncon(a, b):
	'return not a and b AKA ¬(a->b) AKA ¬a∧b AKA negation(converse_implication(a,b))'
	return not a and b

def _cot_cmath(x):
	'trigonometric cotangent (using cmath)'
	return 1/_cmath.tan(x)

def _sec_cmath(x):
	'trigonometric secant (using cmath)'
	return 1/_cmath.cos(x)

def _csc_cmath(x):
	'trigonometric cosecant (using cmath)'
	return 1/_cmath.sin(x)

def _acot_cmath(x):
	'inverse trigonometric cotangent (using cmath)'
	return _cmath.atan(1/x)

def _asec_cmath(x):
	'inverse trigonometric secant (using cmath)'
	return _cmath.acos(1/x)

def _acsc_cmath(x):
	'inverse trigonometric cosecant (using cmath)'
	return _cmath.asin(1/x)

def _coth_cmath(x):
	'hyperbolic cotangent (using cmath)'
	return 1/_cmath.tanh(x)

def _sech_cmath(x):
	'hyperbolic secant (using cmath)'
	return 1/_cmath.cosh(x)

def _csch_cmath(x):
	'hyperbolic cosecant (using cmath)'
	return 1/_cmath.sinh(x)

def _acoth_cmath(x):
	'inverse hyperbolic cotangent (using cmath)'
	return _cmath.atanh(1/x)

def _asech_cmath(x):
	'inverse hyperbolic secant (using cmath)'
	return _cmath.acosh(1/x)

def _acsch_cmath(x):
	'inverse hyperbolic cosecant (using cmath)'
	return _cmath.asinh(1/x)

def _dist(*args):
	'euclidean distance in n dimensions'
	from math import sqrt
	return sqrt(sum(arg**2 for arg in args))

#default = _DotDict()

default = {
# arithmetic
'add'     : _operator.add,
'sub'     : _operator.sub,
'mul'     : _operator.mul,
'div'     : _operator.truediv,

# numeric
'pos'     : _operator.pos,	  # unary plus, positive
'neg'     : _operator.neg,    # unary minus, negative, additive inverse
'mod'     : _operator.mod,
'floordiv': _operator.floordiv,
'abs'     : _operator.abs,
'inv'     : _reciprocal,      # multiplicative inverse
'square'  : _square,
'cube'    : _cube,
'pow'     : _builtins.pow,
'floor'   : _math.floor,
'round'   : _builtins.round,
'ceil'    : _math.ceil,
'ipart'   : _math.trunc,
'fpart'   : _fractional_part,
'exp'     : _math.exp,
'exp2'    : _math.exp2,
'log10'   : _math.log10,
'log2'    : _math.log2,
'log'     : _math.log,
'sqrt'    : _math.sqrt,
'cbrt'    : _math.cbrt,
'root'    : _root,

# trigonometric
'sin'     : _math.sin,
'cos'     : _math.cos,
'tan'     : _math.tan,
'cot'     : _cot,
'sec'     : _sec,
'csc'     : _csc,
'asin'    : _math.asin,
'acos'    : _math.acos,
'atan'    : _math.atan,
'acot'    : _acot,
'asec'    : _asec,
'acsc'    : _acsc,

# hyperbolic
'sinh'    : _math.sinh,
'cosh'    : _math.cosh,
'tanh'    : _math.tanh,
'coth'    : _coth,
'sech'    : _sech,
'csch'    : _csch,
'asinh'   : _math.asinh,
'acosh'   : _math.acosh,
'atanh'   : _math.atanh,
'acoth'   : _acoth,
'asech'   : _asech,
'acsch'   : _acsch,

# left out due to obscurity. also probably mostly wrong :P
#'versin'    : lambda a: 1 - math.cos(a)
#'coversin'  : lambda a: 1 - math.sin(a)
#'haversin'  : lambda a: 0.5 - math.cos(a)/2
#'hacoversin': lambda a: 0.5 - math.sin(a)/2
#'exsec'     : lambda a: 1/math.cos(a) - 1
#'excsc'     : lambda a: 1/math.sin(a) - 1
#'chord'     : lambda a: 2 * math.sin(a/2)
#'vercos'    : lambda a: 1 + math.cos(a)
#'covercos'  : lambda a: 1 + math.sin(a)
#'havercos'  : lambda a: 0.5 + math.cos(a)/2
#'hacovercos': lambda a: 0.5 + math.sin(a)/2

# complex
'real'    : _get_real, # get real lmao
'imag'    : _get_imag,
'phase'   : _cmath.phase,
'conj'    : _call_conjugate,

# boolean
'truth'   : _operator.truth,       # 01
'not'     : _operator.not_,        # 10
'and'     : _operator.and_,        # 0001
'nimp'    : _nimp,                 # 0010
'ncon'    : _ncon,                 # 0100
'xor'     : _operator.xor,         # 0110
'or'      : _operator.or_,         # 0111
'nor'     : _nor,                  # 1000
'xnor'    : _operator.eq,          # 1001
'con'     : _converse_implication, # 1011
'imp'     : _implication,          # 1101
'nand'    : _nand,                 # 1110

# comparative
'lt'      : _operator.lt,
'le'      : _operator.le,
'eq'      : _operator.eq,
'ne'      : _operator.ne,
'ge'      : _operator.ge,
'gt'      : _operator.gt,

# statistical
'mean'    : _mean,
'median'  : _median,
'mode'    : _mode,
'pmean'   : _generalized_mean,

# combinatorial
'comb'    : _math.comb,
'perm'    : _math.perm,

# hello there! lol

# bitwise
'bittruth': lambda a: a,
'bitnot'  : _operator.invert,      # 10
'bitand'  : _operator.and_,        # 0001
'bitor'   : _operator.or_,         # 0111
'bitnand' : _nand,                 # 1110
'bitnor'  : _nor,                  # 1000
'bitxor'  : _operator.xor,         # 0110
'bitxnor' : _operator.eq,          # 1001
'bitimp'  : _implication,          # 1101
'bitcon'  : _converse_implication, # 1011
'bitnimp' : _nimp,                 # 0010
'bitncon' : _ncon,                 # 0100
'lshift'  : _operator.lshift,
'rshift'  : _operator.rshift,

# miscellaneous
'dist'    : _dist,
'any'     : _builtins.any,
'all'     : _builtins.all,
'len'     : _builtins.len,
'range'   : _builtins.range,
'reversed': _builtins.reversed,
'sorted'  : _builtins.sorted,
'divmod'  : _builtins.divmod,
'call'    : _operator.call,
'matmul'  : _operator.matmul,
'concat'  : _operator.concat,
'sign'    : _signum,
'ifelse'  : _ifelse,
'fact'    : _math.factorial,
'gamma'   : _math.gamma,
'sumt'    : _sumtorial,
'gcd'     : _math.gcd,
'lcm'     : _math.lcm,
'clamp'   : _clamp,
'lerp'    : _lerp,
'unlerp'  : _unlerp,
'min'     : _builtins.min,
'max'     : _builtins.max,
'is'      : _operator.is_,
'isnot'   : _operator.is_not,
#'erf'     : _math.erf
#'erfc'    : _math.erfc
#'in'      : 
#'notin'   : 

# datatyping
'tuple'   : _to_tuple,
'list'    : _to_list,
'dict'    : _to_dict,
'set'     : _to_set,
}

complex = default.copy()

complex.update({
# trigonometric
'sin'   : _cmath.sin,
'cos'   : _cmath.cos,
'tan'   : _cmath.tan,
'cot'   : _cot_cmath,
'sec'   : _sec_cmath,
'csc'   : _csc_cmath,
'asin'  : _cmath.asin,
'acos'  : _cmath.acos,
'atan'  : _cmath.atan,
'acot'  : _acot_cmath,
'asec'  : _asec_cmath,
'acsc'  : _acsc_cmath,

# hyperbolic
'sinh'  : _cmath.sinh,
'cosh'  : _cmath.cosh,
'tanh'  : _cmath.tanh,
'coth'  : _coth_cmath,
'sech'  : _sech_cmath,
'csch'  : _csch_cmath,
'asinh' : _cmath.asinh,
'acosh' : _cmath.acosh,
'atanh' : _cmath.atanh,
'acoth' : _acoth_cmath,
'asech' : _asech_cmath,
'acsch' : _acsch_cmath
})
"""
# operators and their arity
default2 = {
# arithmetic

'pos'     : (_operator.pos,     1) # unary plus, positive
'neg'     : (_operator.neg,     1) # unary minus, negative, additive inverse
'mod'     : (_operator.mod,     1)
'abs'     : (_operator.abs,     1)
'inv'     : (_reciprocal,       1) # multiplicative inverse
'square'  : (_square,           1)
'cube'    : (_cube,             1)
'floor'   : (_math.floor,       1)
'ceil'    : (_math.ceil,        1)
'ipart'   : (_math.trunc,       1)
'fpart'   : (_fractional_part,  1)
'exp2'    : (_math.exp2,        1)
'log10'   : (_math.log10,       1)
'log2'    : (_math.log2,        1)
'sqrt'    : (_math.sqrt,        1)
'cbrt'    : (_math.cbrt,        1)
'add'     : (_operator.add,     2)
'sub'     : (_operator.sub,     2)
'mul'     : (_operator.mul,     2)
'div'     : (_operator.truediv, 2)
'floordiv': (_operator.floordiv,2)
'pow'     : (_builtins.pow,     2)
'round'   : (_builtins.round,   2)
'exp'     : (_math.exp,         2)
'log'     : (_math.log,         2)
'root'    : (_root,             2)
}
"""
