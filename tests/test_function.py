import gapprox as ga

x = ga.Symbol('x')
e = ga.Expression.from_str('2+x', {x})
f = ga.Function({x: ga.domains.real}, ga.domains.real, e)

assert f({x: 2}) == 4
