import gapprox as ga

l = [None]*20

l[1] = ga.Number()
l[2] = ga.ScalarNumber()
l[3] = ga.CompositeNumber()
l[4] = ga.Hypercomplex()
l[5] = ga.Natural(2)
l[6] = ga.Whole(3)
l[7] = ga.Integer(4)
l[8] = ga.Rational(3.14)
l[9] = ga.Irrational('pi')
l[10] = ga.Real(1.414)
l[11] = ga.Imaginary(2)
l[12] = ga.Complex(ga.Natural(1),ga.Integer(2))
l[13] = ga.SplitComplex(l[5], l[6])
l[14] = ga.Dual(l[7], l[8])
l[15] = ga.Quaternion(l[5], l[6], l[7], l[8])
l[16] = ga.Octonion(l[15], l[15])
l[17] = ga.Natural(True)
l[18] = ga.Whole(False)
l[19] = ga.Integer(False)

for index, thing in enumerate(l):
	print(index, thing)

for index, thing in enumerate(l):
	print(index, repr(thing))
