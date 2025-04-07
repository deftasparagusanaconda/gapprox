# predictor() takes history and returns params
# history is an array of (error, params)
# params is a tuple of parameters

# adds step_size to a random param at a time 
def random_step(error_history, params_history, step_size=1):
	from random import randrange
	params_new = list(params_history[-1])
	params_new[randrange(0,len(params_new))] += step_size

	return params_new

# i think you should implement:
# greedy descent, gradient descent, momentum descent, ...
# newton's method, bfgs (and lbfgs),
# simulated annealing, evolutionary/genetic algorithm, particle swarm optimization, bayesian optimization, AI (like RL-based optimizers)
# do families like the runge-kutta for ODEs work for this? somehow?
