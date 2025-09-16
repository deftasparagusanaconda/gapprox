import gapprox as ga

var1 = ga.Variable('x')
var2 = ga.Variable('y')
param1 = ga.Parameter(3)
param2 = ga.Parameter(2, name='p')
const1 = ga.constants.pi
const2 = ga.constants.e

symbols = [var1, var2, param1, param2, const1, const2]

def test_basic():
	f = ga.Function('2+x', *symbols)

#f = ga.Function('3*x**e + p*x**p + sin(pi*y)')
