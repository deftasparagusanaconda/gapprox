# nullary boolean functions

#def boolean_False():
#	"boolean False"
#	return False

#def boolean_True():
#	"boolean True"
#	return True

# unary comparison operations

def identity(a):
	"identity"
	return a

def flip(a):
	"-"
	return -a

#def bitwise_identity(a):
#	"bitwise identity"
#	return a

def bitwise_flip(a):
	"bitwise flip"
	return ~a

def boolean_identity(a):
	"boolean identity"
	return True if a else False

def boolean_flip(a):
	"boolean flip"
	return False if a else True

#def abs(a):
#    "abs"
#    return _abs(a)

# binary comparison operations

def lt(a, b):
    "<"
    return a < b

def le(a, b):
    "<="
    return a <= b

def eq(a, b):
    "=="
    return a == b

def ne(a, b):
    "!="
    return a != b

def ge(a, b):
    ">="
    return a >= b

def gt(a, b):
    ">"
    return a > b

def is_(a, b):
    "is"
    return a is b

def is_not(a, b):
    "is not"
    return a is not b

# Mathematical/Bitwise Operations *********************************************#

def add(a, b):
    "+"
    return a + b

def and_(a, b):
    "&"
    return a & b

def floordiv(a, b):
    "//"
    return a // b

#def index(a):
#    "Same as a.__index__()."
#    return a.__index__()

def lshift(a, b):
    "<<"
    return a << b

def mod(a, b):
    "%"
    return a % b

def mul(a, b):
    "*"
    return a * b

def matmul(a, b):
    "@"
    return a @ b

def or_(a, b):
    "Same as a | b."
    return a | b

def pow(a, b):
    "Same as a ** b."
    return a ** b

def rshift(a, b):
    "Same as a >> b."
    return a >> b

def sub(a, b):
    "Same as a - b."
    return a - b

def truediv(a, b):
    "Same as a / b."
    return a / b

def xor(a, b):
    "Same as a ^ b."
    return a ^ b

