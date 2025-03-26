# stepper() takes history and returns params
# history is an array of (error, params)
# params is a tuple of parameters

import random

# adds step_size to a random param at a time 
def greedy_GD(error_history, params_history, step_size=1):
	params_new = list(params_history[-1])
	params_new[random.randrange(0,len(params_new))] += step_size

	return params_new
