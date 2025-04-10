# optimizer is an instance of Optimizer
# the object manages your current configuration of expression, error, predictor, ...
# it also exposes its components as modules

from . import predictors, errors, cold_starters, utils

# store multithreading configuration
class WorkerConfig:
	# instance variables
	def __init__(self):
		self.threads:int = 0		# 0 = automatic
		self.end_condition_modes:list[str] = ["any", "all"]
		self.competition_modes:list[str] = ["linear", "parallel"]
		self.competition_mode:str = "linear"

class EndConditions:
	# static variables
	check_modes = ["any", "all"]
	
	# instance variables
	def __init__(self):
		self.check_mode = "any"
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
	
#	def check() -> bool:
#		if check_mode == "any":
#			print("i havent implemented this yet")
#		return False
		
class Optimizer:
	# expose modules
	predictors = predictors
	errors = errors
	cold_starters = cold_starters
		
	# instance variables
	def __init__(self):
		# store configuration 
		self.predictor = predictors.bfgs
		self.error = errors.smape
		self.cold_starter = cold_starters.zeroes
		self.keep_regressive_errors:bool = False
		self.store_output_history:bool = True
		self.live_output_update:bool = True
		self.history_length:int = 10		# magic default. we really need to make a better default. why is 10 good??? think of something better! you cant just say "oh, 10 might be good" and slap some magic numbers on code!
		self.end_condition_mode:str = "any"
		self.workers = WorkerConfig()
		
		self.error_history = []
		self.parameters_history = []
		self.output_history = []
		self.iter_count:int = 0
	
	def iterate(self, ga):
		"""run one iteration of the optimizer"""
		if len(self.error_history) != len(self.parameters_history):
			raise ValueError(f"history length mismatch: len(error_history)={len(self.error_history)}, len(parameters_history)={len(self.parameters_history)}")

		# first iteration case ----------
		if not self.error_history:
			# get parameters
			if ga.generator:
				new_parameters = ga.generator(ga.input)
			else:
				if self.cold_starter:
					new_parameters = self.cold_starter(len(ga.input))	# not sure for now. depends on cold_start
				else:
					new_parameters = ga.input
					utils.warn("neither generator nor optimizer.cold_starter defined! taking ga.input as starting parameters...\nthis is not intended behaviour. are you sure?\notherwise, define generator or define optimizer.cold_starter")


			# get output
			if ga.expression:
				new_output = ga.expression(new_parameters)
			else:
				new_output = new_parameters
				utils.warn("no expression defined. passing parameters as output...\nthis is not intended behaviour. are you sure?\notherwise, define expression")
			# get error
			new_error = self.error(ga.input, new_output)

			# chores
			self.error_history.append(new_error)
			self.parameters_history.append(new_parameters)
			if self.store_output_history:
				self.output_history.append(new_output)
			if self.live_output_update:
				ga.output = new_output
			if len(self.error_history) > self.history_length:
				self.error_history.pop(0)
				self.parameters_history.pop(0)
				try:
					self.output_history.pop(0)
				except:
					pass
			# dinky code but it works for now
			
			self.iter_count += 1
			# no keep_regressive_errors check needed
		
			return new_output

		# normal iteration case ----------
	
		# get parameters
		new_parameters = self.predictor(self.error_history, self.parameters_history)

		# get output
		if ga.expression:
			new_output = ga.expression(new_parameters)
		else:
			new_output = new_parameters
			utils.warn("no expression defined. passing parameters as output...\nthis is not intended behaviour. are you sure?\notherwise, define expression")
		# get error
		new_error = self.error(ga.input, new_output)

		if not self.keep_regressive_errors and new_error > self.error_history[-1]:
			return None

		# chores
		self.error_history.append(new_error)
		self.parameters_history.append(new_parameters)
		if self.store_output_history:
			self.output_history.append(new_output)
		if self.live_output_update:
			ga.output = new_output
		self.iter_count += 1

		return new_output

	"""i want the multithreading to support two modes (or more in the future!): linear competition and parallel competition

linear competition: threads compete for the next best iteration
parallel competition: threads go off on their own for a few iterations. then come back and compare against each other. parallel competition mode will take a variable that determines how often they come together again to choose a new alpha of the pack! hehehehe"""
	
	# these three competition modes will be replaced inline into __call__(). for now, this is for brainstorming
	def _competition_single(self, ga):	# kinda ironic that were calling a competition but theres only one competitor. poor lonely thread lol
		iter_limit = 100	# magic number, for testing for now...
		for _ in range(iter_limit):
			self.iterate(ga)

	def _competition_parallel(self, ga):
		print("not made yet! come back later!")
#		census_modes = ["iter","time"]
#		census_mode = "iter"
# 	should competition_parallel call a census when a thread runs a number of iterations? or when all threads run a number of iterations? or when their average reaches that amount? or what?
#	should 
#
	def _competition_linear(self, ga):
		print("not made yet! lol")
			
	def optimize(self, ga):
		"""iteratively calculate the most optimal solution"""
		"""
		if self.workers.threads == 1:
			output = self.competition_single(ga)
			return output
		
		import multiprocessing
		if self.workers.threads is None or self.workers.threads == 0:
			threads = multiprocessing.cpu_count()
		else:
			threads = self.workers.threads
		
		if self.workers.competition_mode == "linear":
			output = self.competition_linear(ga)
		elif self.workers.competition_mode == "parallel":
			output = self.competition_parallel(ga)
		else:
			print("invalid competition mode")
			output = None
		"""
		
		return self._competition_single(ga)
	__call__ = optimize	# optimizer.optimize() and optimizer() are same
	
	# basically what you see when you do `print(optimizer)` in the python interpreter
	def __repr__(self):
		return f"<Optimizer instance & module 'optimizer' at {hex(id(self))}>"
	
	def new(self):                  # foo = optimizer.new() creates new instance
		"""return a new instance of Optimizer"""
		return type(self)()

	def copy(self):                 # foo = optimizer.copy() creates a copy
		"""returns a copy of the current Optimizer instance"""
		from copy import deepcopy
		return deepcopy(self)

"""

windowed stagnation can support weighting, but that might be way overkill for something just checking an end condition
otherwise, if weighted windowed stagnation is to be supported, there should be a gradual weighting, where newer values weigh more and older values weigh less

the algorithm can actually take any of these at the same time
it would just end at the condition it reaches first
no.. wait.. ah! problem! if multiple end conditions, how to decide when to end? when one, or all? or some?
"""

# to do:
# implement histories as queues with length history_length

# Optimizer uses a predictor -> objective model
# the convention in ML (machine learning) is objective -> predictor


# need to add debugging prints
# learn to use debugging to print live updates on terminal

# optimizer almost makes sense as a standalone. it depends on ga only as variable storage
# from ga, it uses: input, output, generator, expression
# so maybe change to optimize(self, input, output, generator, expression)?
# to make it more ga-independent
