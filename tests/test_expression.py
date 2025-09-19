import gapprox as ga

def test1():
	f = ga.Expression('2+x')

def test2():
	f = ga.Expression('2+x')

	assert f(x=2) == 4

def test3():
	f = ga.Expression('sin(x)')
	assert f(x=0) == 0

def test4():
	f = ga.Expression('2 < x')
	g = ga.Expression('2 < x < 3')

	assert f(x=0) == False
	assert f(x=2.5) == True
	assert g(x=1) == False
	assert g(x=2.5) == True
	assert g(x=4) == False

def test5():
	'initialization test. i dont know what this should actually evaluate to lmao'
	f = ga.Expression('2 < x == 4 >= y > 3')

"""
for i in range(2):
    for j in range(2):
        for k in range(2):
            print(f"[{bool(i)}, {bool(j)}, {bool(k)}, {bool(i and j or k)}],")

[False, False, False, False],
[False, False, True, True],
[False, True, False, False],
[False, True, True, True],
[True, False, False, False],
[True, False, True, True],
[True, True, False, True],
[True, True, True, True],
"""

def test6():
	f = ga.Expression('x and y or z')

	cases = [
		[False, False, False, False],
		[False, False, True, True],
		[False, True, False, False],
		[False, True, True, True],
		[True, False, False, False],
		[True, False, True, True],
		[True, True, False, True],
		[True, True, True, True]]
	
	for case in cases:
		assert f(x=case[0], y=case[1], z=case[2]) == case[3]

def test7():
	f = ga.Expression('x or y and z')

	cases = [
		[False, False, False, False],
		[False, False, True, False],
		[False, True, False, False],
		[False, True, True, True],
		[True, False, False, True],
		[True, False, True, True],
		[True, True, False, True],
		[True, True, True, True]]

	for case in cases:
		assert f(x=case[0], y=case[1], z=case[2]) == case[3]

def test8():
	f = ga.Expression('x and y and z')

	cases = [
		[False, False, False, False],
		[False, False, True, False],
		[False, True, False, False],
		[False, True, True, False],
		[True, False, False, False],
		[True, False, True, False],
		[True, True, False, False],
		[True, True, True, True]]

	for case in cases:
		assert f(x=case[0], y=case[1], z=case[2]) == case[3]

def test8():
	f = ga.Expression('x or y or z')

	cases = [
		[False, False, False, False],
		[False, False, True, True],
		[False, True, False, True],
		[False, True, True, True],
		[True, False, False, True],
		[True, False, True, True],
		[True, True, False, True],
		[True, True, True, True]]
	
	for case in cases:
		assert f(x=case[0], y=case[1], z=case[2]) == case[3]

"""
for i in range(2):
    for j in range(2):
        for k in range(2):
            print(f"[{bool(i)}, {bool(j)}, {bool(k)}, {bool(i if j else k)}],")

[False, False, False, False],
[False, False, True, True],
[False, True, False, False],
[False, True, True, False],
[True, False, False, False],
[True, False, True, True],
[True, True, False, True],
[True, True, True, True],
"""


def test9():
	f = ga.Expression('x if y else z')

	cases = [
		[False, False, False, False],
		[False, False, True, True],
		[False, True, False, False],
		[False, True, True, False],
		[True, False, False, False],
		[True, False, True, True],
		[True, True, False, True],
		[True, True, True, True]]
		
	for case in cases:
		assert f(x=case[0], y=case[1], z=case[2]) == case[3]

#f = ga.Expression('3*x**e + p*x**p + sin(pi*y)')

def test10():
	expr = 'sin(x + y) * cos(z) + log(abs(x*y - z + 1)) + exp(sin(y) * cos(x)) + (x**2 + y**2 + z**2)**0.5 + tanh(x*y - z) + sqrt(abs(sin(x*z) + cos(y))) + (log(abs(x+1)) + exp(y*z) - sin(z)) / (1 + x**2 + y**2)'
	f = ga.Expression(expr)

"""
import gapprox as ga
x, y, z = ga.make_variables('x', 'y', 'z')
expr = 'sin(x + y) * cos(z) + log(abs(x*y - z + 1)) + exp(sin(y) * cos(x)) + (x**2 + y**2 + z**2)**0.5 + tanh(x*y - z) + sqrt(abs(sin(x*z) + cos(y))) + (log(abs(x+1)) + exp(y*z) - sin(z)) / (1 + x**2 + y**2)'
f = ga.Expression(expr, x, y, z)
f.dag.visualize()
"""
