from abc import ABC as _ABC
from collections.abc import Callable as _Callable, Sequence as _Sequence
from collections.abc import MutableSequence as _MutableSequence	# for GreedyLocalSearch.default_state
from inspect import Signature as _Signature, BoundArguments as _BoundArguments, Parameter as _Parameter	# for parameters
from abc import abstractmethod as _abstractmethod
import random as _random
from typing import Any as _Any

class Optimizer(_ABC):
	'abstract base class for iterative optimization'

class StructureOptimizer(Optimizer):
	...

class ParameterOptimizerStrategy:
	# super cool function that can bind arguments using python's inspect.Signature. really really cool. now we dont have to rely on an odict
	def __init__(self, 
			objective: _Callable, 	# the function to optimize parameters for
			comparers: _Sequence[_Callable[[...], bool]],	# the ordering functions that work on the vector output of the objective
			parameters: None | _Signature = None	# the parameters that we mutate (yes, its the mutable thing)
			):
		'if parameters is not given, it is inferred from the objective callable'

		self.objective: _Callable = objective
		self.comparers: _Sequence[_Callable[[...], bool]] = comparers
		self.parameters: None | _Signature = parameters

		if self.parameters is None:
			# infer signature from the callable objective
			self.parameters: _Signature = _Signature.from_callable(objective)
		
		assert isinstance(self.parameters, _Signature)
	
	@property
	@_abstractmethod
	def default_state(self) -> _Any:
		'the state object that the caller should remember so that the optimizer is stateful'
		...
	
	@_abstractmethod
	def optimize(self,
			*,
			state: _Any,
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		...

	__call__ = optimize

def _bind_all(signature: _Signature, bind_value: _Any, *, use_defaults: bool = True) -> _BoundArguments:
	args: _MutableSequence[_Any] = []
	kwargs: dict = {}
	
	for parameter in signature.parameters.values():
		if use_defaults and parameter.default is not _Parameter.empty:
			continue

		match parameter.kind:
			case _Parameter.POSITIONAL_ONLY:
				args.append(bind_value)
			case _Parameter.POSITIONAL_OR_KEYWORD:
				args.append(bind_value)
			#case _Parameter.VAR_POSITIONAL:
			#	args.extend(())
			case _Parameter.KEYWORD_ONLY:
				kwargs[parameter.name] = bind_value
			#case _Parameter.VAR_KEYWORD:
			#	kwargs.update({})

	bound_arguments: _BoundArguments = signature.bind(*args, **kwargs)

	if use_defaults:
		bound_arguments.apply_defaults()

	return bound_arguments

class GreedyLocalSearch(ParameterOptimizerStrategy):
	'the state object only remembers the last improvement point'
	@property
	def default_state(self, *, default_x: _Any = 0.0, default_y: _Any = 0.0, use_signature_defaults: bool = True) -> _MutableSequence[_BoundArguments, _Any]:
		x: _BoundArguments = _bind_all(self.parameters, default_x, use_defaults = use_signature_defaults)
		y: _Any = default_y
		return [x, y]
	
	def optimize(self, 
			iterations: int,
			step: int,
			*, 
			state: _MutableSequence[_BoundArguments, float],
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:

		# initialize pareto_front
		if pareto_front is None:
			pareto_front = set()
		
		for _ in range(iterations):
			x_old, y_old = state
			
			# craft x_new
			x_new_args: tuple = (x + _random.uniform(-step, step) for x in x_old.args)
			x_new_kwargs: dict = {name: x + _random.uniform(-step, step) for name, x in x_old.kwargs.items()}
			x_new: _BoundArguments = self.parameters.bind(*x_new_args, **x_new_kwargs)

			y_new: _Sequence[float] = self.objective(*x_new.args, **x_new.kwargs)
			
			# if a pareto point is found
			if any(comparer(y_old, y_new) for comparer in self.comparers):
				state = [x_new, y_new]
				point: tuple = x_new, y_new
				pareto_front.add(point)

		return pareto_front

class ParameterOptimizer(Optimizer):
	def __init__(self, strategy: ParameterOptimizerStrategy):
		self._strategy: ParameterOptimizerStrategy = strategy
	
	def default_state(self) -> _Any:
		return self._strategy.default_state
	
	def optimize(self, 
			*args, 
			state: _Any, 
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			**kwargs
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		return self._strategy.optimize(*args, state = state, pareto_front = pareto_front, **kwargs)

	__call__ = optimize

def myfunc(x):
	return (x - 3) ** 2

def is_better(old, new) -> bool:
	return new < old
	
paramoptim = GreedyLocalSearch(myfunc, [is_better])
state = paramoptim.default_state
result = paramoptim.optimize(iterations = 1000, step = 0.1, state = state)
print(result)

# NOTE: using _Sequence[_Callable[[...], bool] for the comparers assumes that the objective function will return the objectives as a tuple. it might not always, so find a cleaner abstraction for this.
# NOTE: likewise, using set[tuple[_BoundArgument, _Sequence[_Any]]] for the pareto front also assumes that the objective returns objectives as a tuple
# stupid. the objectives could even come out as a dict! dont assume. please reabstract this.

# ------------------------------------------------------------------------------

'''
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

#	def show(self):
#		print("should print end conditions here")
	
#	def check() -> bool:
#		if check_mode == "any":
#			print("i havent implemented this yet")
#		return False

class Optimizer:
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
		'run one iteration of the regressor'
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
	
	def optimize(self, input_params, input_actual, expression):
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

'i want the multithreading to support two modes (or more in the future!): linear competition and parallel competition'

'linear competition: threads compete for the next best iteration'
'parallel competition: threads go off on their own for a few iterations. then come back and compare against each other. parallel competition mode will take a variable that determines how often they come together again to choose a new alpha of the pack! hehehehe'

# Regressor uses a predictor -> objective model
# the convention in ML (machine learning) is objective -> predictor

# need to add debugging prints
# learn to use debugging to print live updates on terminal

'''
