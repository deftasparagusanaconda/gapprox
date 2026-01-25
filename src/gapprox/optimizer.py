from abc import ABC as _ABC
from collections.abc import Callable as _Callable, Sequence as _Sequence
from collections.abc import MutableSequence as _MutableSequence	# for GreedyLocalSearch.default_history
from inspect import Signature as _Signature, BoundArguments as _BoundArguments, Parameter as _Parameter	# for parameters
from abc import abstractmethod as _abstractmethod
import random as _random
from typing import Any as _Any
from collections import deque as _deque, namedtuple as _namedtuple	# for history objects
from .objective import Objective

HistoryTuple: _namedtuple = _namedtuple('HistoryTuple', ['inputs', 'input_rewards', 'outputs', 'output_rewards'])

class Optimizer(_ABC):
	'abstract base class for iterative optimization'

class StructureOptimizer(Optimizer):
	...

def _bind_all(signature: _Signature, bind_value: _Any, *, use_defaults: bool) -> _BoundArguments:
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

class ParameterOptimizerStrategy:
	"the optimizer assumes that any exposed parameter on the objective function is available for optimization, exactly as it should assume. after all, its in the name. 'parameter'"
	def __init__(self, objective: _Objective):
		if not isinstance(objective, _Objective):
			raise TypeError(f'{objective} should be an instance of Objective')
		self.objective: _Objective = objective
		
	@property
	def default_history(
			self, 
			maxsize: int,
			*, 
			default_input_value         : _Any = 0.0, 
			default_output_value        : _Any = 0.0, 
			default_input_rewards_value : _Any = float('-inf'),
			default_output_rewards_value: _Any = float('-inf'),
			use_defaults: bool = True
			) -> _HistoryTuple[
				_deque[tuple[...] | dict[str, ...] | BoundArguments],
				_deque[tuple[...] | dict[str, ...] | BoundArguments],
				_deque[tuple[...] | dict[str, ...] | BoundArguments],
				_deque[tuple[...] | dict[str, ...] | BoundArguments]]:
		
		signature: _Signature = _Signature.from_callable(self.objective)
		for parameter in _signature.




		_bind_all(self.parameters, default_input, use_defaults = use_defaults)

		old_input_rewards : tuple[...] | dict[str, ...] | BoundArguments = 
		old_outputs       : tuple | dict | BoundArguments = 
		old_output_rewards: tuple | dict | BoundArguments = 
		return HistoryTuple(input)	
	
	@_abstractmethod
	def optimize(self,
			*,
			history: _Any,
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		...

	__call__ = optimize

class GreedyLocalSearch(ParameterOptimizerStrategy):
	def optimize(self, 
			iterations: int,
			step: float,
			*, 
			history: HistoryTuple[_deque, _deque, _deque, _deque],
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		
		# the .optimize method will work with the following objects:
		# objfunc.input_args: tuple[...]        # parameter rewarders
		# objfunc.input_kwargs: tuple[...]      # parameter rewarders
		# objfunc.output_args: tuple[...]       # objective rewarders
		# objfunc.output_kwargs: tuple[...]     # objective rewarders
		# objfunc.input_args[0].input_args      # parameter rewarder … args
		# objfunc.input_args[0].input_kwargs    # parameter rewarder … kwargs
		# objfunc.input_kwargs[0].input_args    # parameter rewarder … args
		# objfunc.input_kwargs[0].input_kwargs  # parameter rewarder … kwargs
		# …
		# objfunc.output_args[0].input_args     # parameter rewarder … args
		# objfunc.output_args[0].input_kwargs   # parameter rewarder … kwargs
		# objfunc.output_kwargs[0].input_args   # parameter rewarder … args
		# objfunc.output_kwargs[0].input_kwargs # parameter rewarder … kwargs
		# …
		# for each parameter and objective, it calls its corresponding rewarder.
		# for each rewarder, it uses its corresponding .input_* to fill in any arguments
		
		# initialize pareto_front
		pareto_front: set = set() if pareto_front is None else pareto_front
		
		# lets visualize this to create this
		# 
		# @input_metadata(None, None, None)
		# @output_metadata(rewarders.maximize, rewarders.minimize)
		# def triangle(a, b, c):
		# 	sum = a + b + c
		# 	prod = a * b * c
		# 	
		# 	return sum, prod
		
		# old_inputs        : tuple | dict | BoundArguments = (0.0, 0.0, c = 0.0)
		# old_input_rewards : tuple | dict | BoundArguments = 
		# old_outputs       : tuple | dict | BoundArguments = 
		# old_output_rewards: tuple | dict | BoundArguments = 
		
		for _ in range(iterations):
			old_inputs, old_outputs, old_input_rewards, old_output_rewards = self.history
			
			# create new_input
			new_input_args: tuple[...] = (old_input + _random.choice((-step, step)) for old_input in old_inputs[0])
			new_input_kwargs: dict[str, ...] = {name: val_old + _random.choice((-step, step)) for val_old in input_old}
			
			# create new_output
			new_output = self.objective(*input_new.args, **input_new.kwargs)
			
			# create new_input_rewards
			new_input_rewards = _Objective.evaluate_rewards(new_input_args, self.objective.input_rewarders)

			# create new_output_rewards
			new_output_rewards = _Objective.evaluate_rewards(new_output_args, self.objective.output_rewarders)
			
			'''
			# initialize pareto_front
			if pareto_front is None:
				pareto_front = set()
			
			for _ in range(iterations):
				x_old, y_old = history
				
				# craft x_new
				x_new_args: tuple = (x + _random.uniform(-step, step) for x in x_old.args)
				x_new_kwargs: dict = {name: x + _random.uniform(-step, step) for name, x in x_old.kwargs.items()}
				x_new: _BoundArguments = self.parameters.bind(*x_new_args, **x_new_kwargs)
				
				y_new: _Sequence[float] = self.objective(*x_new.args, **x_new.kwargs)
				
				# if a pareto point is found
				if any(comparer(y_old, y_new) for comparer in self.comparers):
					history = [x_new, y_new]
					point: tuple = x_new, y_new
					pareto_front.add(point)
		
		return pareto_front
		'''

class ParameterOptimizer(Optimizer):
	def __init__(self, strategy: ParameterOptimizerStrategy):
		self._strategy: ParameterOptimizerStrategy = strategy
	
	def default_history(self) -> _Any:
		return self._strategy.default_history
	
	def optimize(self, 
			*args, 
			history: _Any, 
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			**kwargs
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		return self._strategy.optimize(*args, history = history, pareto_front = pareto_front, **kwargs)

	__call__ = optimize
