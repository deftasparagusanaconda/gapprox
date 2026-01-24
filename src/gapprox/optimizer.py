# NOTE: the optimizer assumes that the objective function has an .output_shape attribute, which is an instance of the Shape class. the output_shape decorator is used to give this attribute to the objective function. this is how optimizer knows the shape of the output, without having to guess whether the objective function is scalar-valued or vector-valued

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

# FIXME: sometimes you assume objective is scalar, sometimes you assume its vector. decide on a proper abstraction

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
	
param_optim = GreedyLocalSearch(myfunc, [is_better])
state = param_optim.default_state
result = param_optim.optimize(iterations = 1000, step = 0.1, state = state)
print(result)

# NOTE: using _Sequence[_Callable[[...], bool] for the comparers assumes that the objective function will return the objectives as a tuple. it might not always, so find a cleaner abstraction for this.
# NOTE: likewise, using set[tuple[_BoundArgument, _Sequence[_Any]]] for the pareto front also assumes that the objective returns objectives as a tuple
# stupid. the objectives could even come out as a dict! dont assume. please reabstract this.

