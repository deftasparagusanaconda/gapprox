import gapprox as ga

a = ga.Truth()
b = ga.AtomicTruth()
c = ga.CompositeTruth()
d = ga.Boolean(True)
e = ga.Boolean(False)
f = ga.FuzzyTruth(0.5)
g = ga.FuzzyTruth(2)
h = ga.PolyBoolean(d, e)
i = ga.PolyFuzzyTruth(f, g)
