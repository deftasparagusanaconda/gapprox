# this test file dont work

import optimizer
import numpy as np
import generators
import expressions

class DummyGA:
	def __init__(self):
		self.input = np.array([1.0, 2.0, 3.0])
		self.output = None
		self.generator = generators.line.least_squares
		self.expression = expressions.polynomial.polynomial

opt = optimizer
ga = DummyGA()

print("initial output:", ga.output)
opt(ga)
print("after optimization:", ga.output)

print("error history:", opt.error_history)
print("param history:", opt.parameters_history)

