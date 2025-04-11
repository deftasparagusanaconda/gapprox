import graphapproximator as ga

ga.input = [1,2,3,5,4]
ga.generator = ga.generators.dct.dct
ga.expression = ga.expressions.idct.idct
ga.use_optimizer = True

ga.approximate()
