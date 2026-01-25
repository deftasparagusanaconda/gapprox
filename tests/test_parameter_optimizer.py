import gapprox as ga

def test_greedylocalsearch():
	@ga.input_metadata(None, None, None)	# no constraints on the inputs
	@ga.output_metadata(ga.rewarders.maximize, ga.rewarders.minimize)	# maximize prod, minimize sum
	def triangle(a, b, c):
		prod = a * b * c
		sum = a + b + c
		return prod, sum
	
	param_optim = ga.ParameterOptimizer.from_GreedyLocalSearch(triangle)
	state = param_optim.default_state
	result = param_optim.optimize(iterations = 1000, step = 0.1, state = state)
	print(result)
