import gapprox as ga

from gapprox import Lambda, Domain, Mapping, Relation, Function

def test_Lambda():
	f = ga.Lambda('2+x', 'x')

	assert f(3) == 5

	f = ga.Lambda('3+4*abs(x*y)', 'x', 'y')
	assert f(2, 3) == 27

def test_Domain():
	s1 = ga.Domain({1,2,3})
	s2 = ga.Domain(lambda x: x < 3)
	s3 = ga.Domain(ga.Lambda('x < 2', 'x'))

	assert 2 in s1
	assert 3 in s1
	assert 2 in s2
	assert 3 not in s2
	assert 2 not in s3
	assert 3 not in s3

def test_Mapping():
	m1 = ga.Mapping({'a': 1, 'b': 2})
	m2 = ga.Mapping(lambda a: a ** 2)

	assert m1('a') == 1
	assert m1('b') == 2
	assert m2(2) == 4
	assert m2(16) == 256

#def test_Relation():
#	r1 = ga.Relation()
