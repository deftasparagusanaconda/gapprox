def difference(a, b):
	'b-a'
	return a - b

def difference_absolute(a, b):
	'abs(b-a)'
	return abs(a - b)

def difference_squared(a, b):
	return (a - b)**2

def ratio_a(a, b):
	return (a - b)/b

def ratio_b(a, b):
	return (a - b)/a

def ratio_symmetric(a, b):
	return (a - b)/(b + a)/2

def ratio_symmetric_absolute(a, b):
	return abs(a - b)/(b + a)/2

def ratio_log(a, b):
	from math import log
	return log(a/b)

def relative_difference(a, b):
	return abs(a - b)/(abs(a) + abs(b))/2

