# functions that take purely boolean input and output

"""
00 01 10 11 inputs

0  0  0  0  off
0  0  0  1  a * b (and)
0  0  1  0  a > b
0  0  1  1  a >= b (a)
0  1  0  0  a < b
0  1  0  1  a <= b (b)
0  1  1  0  a != b (xor)
0  1  1  1  a + b (or)
1  0  0  0  !(a+b)(nor)
1  0  0  1  !(a==b) (xnor)
1  0  1  0  !(a<=b) (!b)
1  0  1  1  !(a<b)
1  1  0  0  !(a>=b) (!a)
1  1  0  1  !(a>b)
1  1  1  0  !(a*b) (nand)
1  1  1  1  !off (on)
"""

def flip(a):
	"flip"
	return not a
not_ = flip

def and_(a, b):
	"and"
	return a and b

def or_(a, b):
	"or"
	return a or b

def greater_than(a, b):
	">"
	return a > b

def equal(a, b):
	"=="
	return a == b
xnor = equal
	
def not_equal(a, b):
	"!="
	return a != b
xor = not_equal

def lesser_than(a, b):
	"<"
	return a < b

def any(*args):
	"any"
	return any(args)

def all(*args):
	"all"
	return all(args)
