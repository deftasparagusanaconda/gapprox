import graphapproximator.api as ga

ga.input = [1,2,3,5,4]
ga.generator = ga.generators.dct
ga.expression = ga.expressions.idct

ga.approximate()
ga.show()
