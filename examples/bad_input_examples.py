import gapprox as ga

graph = ga.Engine()

graph.input = 1.2, 2.4, 3.3, 9.7, 1.0		# trying to approximate values
graph.input = (1,2), (2,3), (1,3), (9,10)	# trying to give points
graph.input = [8,4,2,0], [2,3,5,4], [1,2,5,3]	# trying to approximate a surface
graph.input = ([1,2,3,4], [2,5,1,5]), ([2,3,1], [8,8,9,0])	# ragged matrix

graph.input = ([1,2,3,4], [2,5,1,5]), ([2,3,1,3], [8,8,9,0])	# correct example

graph.structgen


graph.approximate()
graph.fit()


