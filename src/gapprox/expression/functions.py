# note that operators are just functions with special symbols and precedence

import math
import operator

# arithmetic operators
add = addition = operator.add
sub = subtract = operator.sub
mul = multiply = operator.mul
div = divide   = operator.truediv

# numeric operators
abs   = absolute                       = operator.abs    # operator._abs instead maybe?
neg   = negate                 = operator.neg    # arithmetic negation
pow   = power                  = operator.pow
floor                          = math.floor
ceil  = ceiling                = math.ceil
integer_part                   = math.trunc
exp   = exponential            = math.exp
log10 = logarithm_base_10      = math.log10
log2  = logarithm_base_2       = math.log2
ln    = logarithm_base_natural = math.log
sqrt  = square_root            = math.sqrt
cbrt  = cube_root              = lambda a: a**(1/3)
root                           = lambda num,base: num**(1/base)
fractional_part                = lambda a: math.modf(a)[0]

# comparison operators
less_than                = operator.lt
less_than_or_equal_to    = operator.le
equal                    = operator.eq
not_equal                = operator.ne
greater_than_or_equal_to = operator.ge
greater_than             = operator.gt

# boolean operators
NOT  = operator.not_
AND  = operator.and_
OR   = operator.or_
NAND = lambda a,b: not(a and b)
NOR  = lambda a,b: not(a or b)
XOR  = lambda a,b: a != b
XNOR = lambda a,b: a == b

# trigonometric functions
sin   = sine_circular           = math.sin
cos   = cosine_circular         = math.cos
tan   = tangent_circular        = math.tan
cot   = cotangent_circular      = lambda a: 1/math.tan(a)
sec   = secant_circular         = lambda a: 1/math.cos(a)
csc   = cosecant_circular       = lambda a: 1/math.sin(a)
asin  = arcsine_circular        = math.asin
acos  = arccosine_circular      = math.acos
atan  = arctangent_circular     = math.atan
acot  = arccotangent_circular   = lambda a: math.atan(1/a)
asec  = arcsecant_circular      = lambda a: math.acos(1/a)
acsc  = arccosecant_circular    = lambda a: math.asin(1/a)
sinh  = sine_hyperbolic         = math.sinh
cosh  = cosine_hyperbolic       = math.cosh
tanh  = tangent_hyperbolic      = math.tanh
coth  = cotangent_hyperbolic    = lambda a: 1/math.tanh(a)
sech  = secant_hyperbolic       = lambda a: 1/math.cosh(a)
csch  = cosecant_hyperbolic     = lambda a: 1/math.sinh(a)
asinh = arcsine_hyperbolic      = math.asinh
acosh = arccosine_hyperbolic    = math.acosh
atanh = arctangent_hyperbolic   = math.atanh
acoth = arccotangent_hyperbolic = lambda a: math.atanh(1/a)
asech = arcsecant_hyperbolic    = lambda a: math.acosh(1/a)
acsch = arccosecant_hyperbolic  = lambda a: math.asinh(1/a)

# miscellaneous functions

ifelse    = lambda cond,yes,no: yes if cond else no
factorial = math.factorial
sumtorial = lambda a: sum(range(1,a+1))

def summation(*args):
	'variadic summation'
	return sum(args)

def product(*args):
	'variadic multiplication'
	return math.prod(args)

def Sigmasummation(expr, (var, lower, upper)):
	'quadric Σ(func(var, lower, upper))'
	return sum(expr(var=val) for value in range(lower, upper))

def Piproduct(expr, (var, lower, upper)):
	'quadric ∏(func(var, lower, upper))'
	return math.prod(expr(var=value) for value in range(lower, upper))

#def Modulus():
#	'binary modulus'

#def Quotient(Node):
#	'binary quotient'

#calculus

def DefiniteIntegral(Node):
	'quadric integral a to b, f(x)dx(func(var, lower, upper))'

def IndefiniteIntegral(Node):
	'binary ∫f(x)dx(func, var)'

def Derivative(Node):
	'binary (func, var)'

def PartialDerivative(Node):
	'variadic(func, var1, var2, ..., varN)'

def Sign (Node):
	'unary -1 or 0 or 1'

def Piecewise(Node):
	'variadic([cond1, val1], [cond2, val2], ....)'

# complex functions

def Real(Node):
	'unary a:a+bi'

def Imag(Node):
	'unary b:a+bi'

def Arg(Node):
	'unary arg'

def Conj(Node):
	'unary a-bi-a+bi'

def Min(Node):
	'variadic min'

def Max(Node):
	'variadic max'

def Clamp(Node):
	'ternary(x, min, max)'

def Gcd(Node):
	'variadic GCD'

def Lcm(Node):
	'variadic LCM'

#other2

def Gamma(Node):
	'unary ¬(x)'

def Limit(Node):
	'quadric (func (var, val, div))'

def Det(Node):
	'|mat|'

def Transpose(Node):
	'mat'

def DotProduct(Node):
	'binary vector A • vector B'

def CrossProduct(Node):
	'binary vector A × vector B'
