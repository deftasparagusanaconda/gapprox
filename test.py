import gapprox as ga

graph = ga.Approximation(
	input = [1,2,3,5,4],
	paramgen = ga.paramgens.dct,
	structgen = ga.structgens.idct
)

graph.evaluate()
graph.summary()
