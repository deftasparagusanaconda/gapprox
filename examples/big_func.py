import gapprox as ga

x, y, z = ga.make_variables('x', 'y', 'z')
expr = 'sin(x + y) * cos(z) + log(abs(x*y - z + 1)) + exp(sin(y) * cos(x)) + (x**2 + y**2 + z**2)**0.5 + tanh(x*y -z) + sqrt(abs(sin(x*z) + cos(y))) + (log(abs(x+1)) + exp(y*z) - sin(z)) / (1 + x**2 + y**2)'
f = ga.Function(expr, x, y, z)
f.dag.visualize()

print(f(1,2,4))
# 503.31175547860823

