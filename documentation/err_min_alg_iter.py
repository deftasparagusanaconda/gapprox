# err_min_alg_iter belongs as a parameterizer, but its unique from the rest in that its iterative

# error_history is a list of errors
# params_history is a list of tuples. the tuples are parameters of expression()

# runs one iteration of a error minimization
# it WILL NOT support multiple iterations
# external code or a wrapper must do that manually

import approximate, expression, error, stepper
from multiprocessing import Pool

def _all_equal(iterable):
	from itertools import groupby
	g = groupby(iterable)
	return next(g, True) and not next(g, False)

def err_min_alg_iter(actual_values, error_history, params_history, func_approx, func_expression, func_error, func_stepper):
	if len(error_history) == 0 and len(params_history) == 0:
		(forecast_params, forecast_values) = func_approx(actual_values, output_type=["params", "values"])
		forecast_error = func_error(actual_values, forecast_values)
		return (forecast_error,forecast_params)
	
	forecast_params = func_stepper(error_history, params_history)
	forecast_values = func_expression(forecast_params)
	forecast_error = func_error(actual_values, forecast_values)
	
	return (forecast_error, forecast_params)

def err_min_alg(actual_values, error_history, params_history, func_approx, func_expression, func_error, func_stepper, end_condition=["interruption"], multithreading=True):
	
	stop_signal = False
	iter_count = 0
	time_count = 0
	
	if 0 == len(error_history) and 0 == len(params_history):
		(forecast_params, forecast_values) = func_expression(func_approx(actual_values), output_type=["params", "values"])
		error_history = [func_error(actual_values, forecast_values)]
		params_history = [forecast_params]
		
	while True:
		forecast_params = func_stepper(error_history, params_history)
		forecast_values = func_expression(forecast_params)
		forecast_error = func_error(actual_values, forecast_values)
		
		if "iter_limit" in end_condition:
			if iter_count > iter_limit:
				break
			else:
				iter_count += 1
		
		if "time_limit" in end_condition:
			if time_count > time_limit:
				break
		
		if "threshold" in end_condition:
			if error_history[-1] <= threshold:
				break
		
		if "reduction_value" in end_condition:
			if error_history[-1] <= error_history[0]-reduction_value:
				break
		
		if "reduction_ratio" in end_condition:
			if error_history[-1] <= error_history[0]/reduction_ratio:
				break
		
		# stagnation conditions:
		if "change_threshold" in end_condition:
			if error_history[-2]-error_history[-1] <= change_threshold:
				break
		
		if "concordancy" in end_condition:
			if _all_equal(error_history[-concordancy:]):
				break
		break
"""
my_actual_values	= [1,2,3,5]
my_error_history	= [1]
my_params_history	= [(2,3,4,5)]
my_func_approx		= approximate.dct
my_func_expression	= expression.idct
my_func_error	 	= error.power_mean
my_func_stepper		= stepper.greedy_GD

print(err_min_alg(my_actual_values,my_error_history, my_params_history, my_func_approx, my_func_expression, my_func_error, my_func_stepper))
"""




"""
implement the following iterator wrappers:
iter_limit		- up to no. of iterations
time_limit		- up to time limit
interruption		- until user manually gives stop signal
threshold		- until error < threshold
reduction_value		- until error is reduced by value amount
reduction_ratio 	- until error is reduced to error/ratio

stagnation conditions (if error does not deviate much after some iterations):
change_threshold	- if error
concordancy		- if the last {concordancy} values all match
inertia(a,b)		- if the last a values didnt achieve more than 

the algorithm can actually take any of these at the same time
it would just end at the condition it reaches first
"""

"""
specifications for a wrapper for iter_err_min_alg()
- support multithreading. one iteration on one thread
- support multiple end conditions
- keep arguments to a minimum
"""
