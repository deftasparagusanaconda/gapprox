# history[] is a list of tuples
# the tuples are (error, params)
# params is also a tuple of parameters

# runs one iteration of a error minimization
# it WILL NOT support multiple iterations. external code must do that manually

# returns tuple of (error, params[])
import approximate, error, stepper
#import sympy

def iter_err_min_alg(actual_values, history, func_approx, func_error, func_stepper):
	
	if len(history) == 0:
		(forecast_params, forecast_values) = func_approx(actual_values, output_type=["params", "values"])
		forecast_error = func_error(actual_values, forecast_values)
		return (forecast_error,forecast_params)
	
	forecast_params = func_stepper(history)
	forecast_values = func_approx(forecast_params, input_type="params")[0]
	forecast_error = func_error(actual_values, forecast_values)

	return (forecast_error, forecast_params)
	
#my_actual_values	= [1,2,3,5]
#my_history		= [(1, (2,3,4,5))]
#my_func_approximate	= approximate.dct
#my_func_error	 	= error.power_mean
#my_func_step		= step.greedy_GD

#print(err_min_alg_iter(my_actual_values,my_history, my_func_approx, my_func_error, my_func_stepper))
