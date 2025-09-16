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
	f = ga.Function('x and y or z', ga.Variable('x'), ga.Variable('y'), ga.Variable('z'))

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
		assert f(case[0], case[1], case[2]) == case[3]

def test7():
	f = ga.Function('x or y and z', ga.Variable('x'), ga.Variable('y'), ga.Variable('z'))

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
		assert f(case[0], case[1], case[2]) == case[3]

def test8():
	f = ga.Function('x and y and z', ga.Variable('x'), ga.Variable('y'), ga.Variable('z'))

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
		assert f(case[0], case[1], case[2]) == case[3]

def test8():
	f = ga.Function('x or y or z', ga.Variable('x'), ga.Variable('y'), ga.Variable('z'))

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
		assert f(case[0], case[1], case[2]) == case[3]

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
	f = ga.Function('x if y else z', ga.Variable('x'), ga.Variable('y'), ga.Variable('z'))

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
		assert f(case[0], case[1], case[2]) == case[3]

#f = ga.Function('3*x**e + p*x**p + sin(pi*y)')
