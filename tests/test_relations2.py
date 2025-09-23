import gapprox as ga

def test_relations():
	d1 = ga.domains.integers
	d2 = ga.Domain({1.1, 2.2, 3.3})

	expr = ga.Expression('2+x')

	assert expr(x=3) == 5

	l1 = ga.Lambda(expr, 'x')

	m1 = lambda a: a*2
	m2 = ga.Mapping({'a': 1, 'b': 2, 'c': 3})
	m3 = ga.Mapping(l1)

	assert l1(4) == 6

	f = ga.Function(d1, d1, m3)
	
	assert f(7) == 9
