# NOTE: regressor is only a parameter regressor for now
# in the future this should be upgraded to a symbolic regressor

# regressor takes parameters and outputs parameters
# it has to know the original input and expression to optimize for

# optimizer is an instance of Optimizer
# the object manages your current configuration of expression, error, predictor, ...
# it also exposes its components as modules

from . import predictors, errors, strategies
from ..api.utils import StatefulFunction

def warn(input):
	print(input)
	# placeholder for now

class EndConditions:
	end_condition_modes:list[str] = ["any", "all"]
	
	# instance variables
	def __init__(self):
		self.end_condition_mode = "any"
		self.interruption = None		# until user manually gives stop signal
		self.iter_limit	= None			# up to no. of iterations
		self.time_limit	= None			# up to time limit
		self.threshold = None			# until error < threshold
		self.reduction_value = None		# until error is reduced by value amount
		self.reduction_ratio = None 		# until error is reduced to error/ratio
		# stagnation conditions (if error does not deviate much after some iterations)
		self.concordancy = None			# if the last n errors all match
		self.change_threshold = None		# if (previous error - new error) < change_threshold
		self.change_slope_threshold = None	# if (average slope of last n errors) < change_slope_threshold
		# windowed stagnation conditions (if the last n values dont achieve enough deviation)
		self.window_range = None		# if (max(last n values)-min(last n values)) < window_range
		self.window_deviation = None		# if deviation(last n values) < window_deviation
		self.window_deviation_weighted=None	# if deviation(last weighted n values) < window_deviation_weighted
	# does putting these in here actually make sense? i dont know. but gotta put em somewhere, right?

	def show(self):
		print("should print end conditions here")
	
#	def check() -> bool:
#		if check_mode == "any":
#			print("i havent implemented this yet")
#		return False

class Regressor:
	_stateful_components = ["predictor", "error", "strategy"]
	# expose modules
	predictors = predictors
	errors = errors
	strategies = strategies
		
	# instance variables
	def __init__(self):
		# store configuration 
		self.strategy = None
		self.predictor = predictors.bfgs
		self.error = errors.smape
		self.keep_regressive_errors:bool = False
		self.store_output_history:bool = True
		self.live_output_update:bool = True
		self.history_length:int = 10		# magic default. we really need to make a better default. why is 10 good??? think of something better! you cant just say "oh, 10 might be good" and slap some magic numbers on code!
		self.end_condition_mode:str = "any"
		self.threads:int = 0	# 0 = automatic
		self.end_conditions = EndConditions()
		
		self.error_history = []
		self.parameters_history = []
		self.output_history = []
		self.iter_count:int = 0
		
	def __setattr__(self, name, value):
		if name in self._stateful_components:
			if value is not None:
				name = StatefulFunction(value)
			else:
				name = None
		else:
			super().__setattr__(name, value)
	
	def iterate(self, input_params, input_actual, expression):
		"""run one iteration of the regressor"""
		if len(self.error_history) != len(self.parameters_history):
			raise ValueError(f"history length mismatch: len(error_history)={len(self.error_history)}, len(parameters_history)={len(self.parameters_history)}")
		
		# get parameters
		new_parameters = self.predictor(self.error_history, self.parameters_history)
		# predictors shall handle things on their own if theres no history

		# get output
		new_output = expression(new_parameters)

		# get error
		new_error = self.error(input_actual, new_output)
		if not self.keep_regressive_errors and len(self.error_history)!=0 and new_error > self.error_history[-1]:
			return None
		
		# chores
		self.error_history.append(new_error)
		self.parameters_history.append(new_parameters)
		if self.store_output_history:
			self.output_history.append(new_output)
#		if self.live_output_update:
#			ga.output = new_output
		self.iter_count += 1

		return new_output
	
	def regress(self, input_params, input_actual, expression):
		return self.strategy(self, input_params, input_actual, expression)
#	optimize = self.strategy
	__call__ = regress	# regressor.regress() and regressor() are same
	
	def show(self):
		print("strategy =", self.strategy)
		print("predictor =", self.predictor)
		print("error =", self.error)
		print("keep_regressive_errors =", self.keep_regressive_errors)
		print("store_output_history =", self.store_output_history)
		print("live_output_update =", self.live_output_update)
		print("history_length =", self.history_length)
		print("end_condition_mode =", self.end_condition_mode)
		print("error_history =", self.error_history)
		print("parameters_history =", self.parameters_history)
		print("output_history =", self.output_history)
		print("iter_count =", self.iter_count)
	
	def show_full(self):
		self.show()
		print()
		print("end_conditions:")
		self.end_conditions.show()
	
	# basically what you see when you do `print(regressor)` in the python interpreter
	def __repr__(self):
		return f"<Regressor instance & module 'regressor' at {hex(id(self))}>"
	
	def new(self):                  # foo = regressor.new() creates new instance
		"""return a new instance of Regressor"""
		return type(self)()

	def copy(self):                 # foo = regressor.copy() creates a copy
		"""returns a copy of the current Regressor instance"""
		from copy import deepcopy
		return deepcopy(self)

"""i want the multithreading to support two modes (or more in the future!): linear competition and parallel competition

linear competition: threads compete for the next best iteration
parallel competition: threads go off on their own for a few iterations. then come back and compare against each other. parallel competition mode will take a variable that determines how often they come together again to choose a new alpha of the pack! hehehehe"""

# Regressor uses a predictor -> objective model
# the convention in ML (machine learning) is objective -> predictor

# need to add debugging prints
# learn to use debugging to print live updates on terminal

