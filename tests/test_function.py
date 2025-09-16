import gapprox as ga

var1 = ga.Variable('x')
var2 = ga.Variable('y')
param1 = ga.Parameter(3)
param2 = ga.Parameter(2, name='p')
const1 = ga.constants.pi
const2 = ga.constants.e

symbols = [var1, var2, param1, param2, const1, const2]

def test1():
	f = ga.Function('2+x', *symbols)

def test2():
	x = ga.Variable('x')
	f = ga.Function('2+x', x)

	assert f(2) == 4

def test3():
	x = ga.Variable('x')
	f = ga.Function('sin(x)', x)

	assert f(0) == 0

def test4():
	x = ga.Variable('x')
	f = ga.Function('2 < x', x)
	g = ga.Function('2 < x < 3', x)

	assert f(0) == False
	assert f(2.5) == True
	assert g(1) == False
	assert g(2.5) == True
	assert g(4) == False

def test5():
	'initialization test. i dont know what this should actually evaluate to lmao'
	f = ga.Function('2 < x == 4 >= y > 3', ga.Variable('x'), ga.Variable('y'))

	
#f = ga.Function('3*x**e + p*x**p + sin(pi*y)')
