import graphapproximator.api as ga

ga.input = [1,2,3,5,4]
ga.analyzer = ga.analyzers.dct
ga.expression = ga.expressions.idct

ga.approximate()
ga.show()
