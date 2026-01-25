import gapprox as ga

def test_greedylocalsearch():
	def parabolae(x, y):
		a = (x - 1) ** 2 + (y - 1) ** 2
		b = -(x ** 2) - (y ** 2)
		return a, b

	objective = ga.Objective(triangle, (ga.rewarders.neutral, ga.rewarders.neutral), (ga.rewarders.minimize, ga.rewarders.maximize))
	
	param_optim = ga.ParameterOptimizer.from_GreedyLocalSearch(objective)
	history = param_optim.get_default_history()
	result = param_optim.optimize(iterations = 10000, step = 0.1, history = history)

	print(result)
'''
import gapprox as ga

def parabolae(x, y):
	a = (x - 1) ** 2 + (y - 1) ** 2
	b = -(x ** 2) - (y ** 2)
	return a, b

objective = ga.Objective(parabolae, (ga.rewarders.neutral, ga.rewarders.neutral), (ga.rewarders.minimize, ga.rewarders.maximize))

param_optim = ga.ParameterOptimizer.from_GreedyLocalSearch(objective)
history = param_optim.get_default_history()
result = param_optim.optimize(iterations = 10000, step = 0.1, history = history)

print(result)
'''
