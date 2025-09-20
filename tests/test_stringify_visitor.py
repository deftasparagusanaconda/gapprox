import gapprox as ga

def test1():
	f = ga.Expression('2+x+x')

	assert f.to_str() == '2 + x + x'
	assert f.to_str(spacing='') == '2+x+x'
	assert f.to_str(spacing='2520') == '22520+2520x2520+2520x'
	assert f.to_str(pretty=True) == '2 + x + x' or f.to_str() == '2+x+x'
