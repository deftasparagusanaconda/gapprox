# stepper() takes history and returns params
# history is an array of (error, params)
# params is a tuple of parameters

import random

# adds step_size to a random param at a time 
def stepper_greedy_GD(history):
	if len(history) == 0:
		raise ValueError("stepper_greedy_GD() received empty history. provide an initial guess")

	step_size = 1
	params_new = list(history[-1][1])
	params_new[random.randrange(0,len(params_new))] += step_size

	return params_new
