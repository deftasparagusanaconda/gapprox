# HOW MANY FKN TIMES AM I GOING TO TRY THIS POS

# lets try to minimize a func

import gapprox as ga
import inspect
from inspect import BoundArguments
from collections.abc import MutableSequence

# minimize a, maximize b
@input_metadata(None, y = None)
@output_metadata(ga.rewarders.minimize, b = ga.rewarders.maximize)
def objfunc(x: float, y: float) -> tuple[float, float]: 
	a = (x - 1) ** 2 + (y - 1) ** 2 
	b = -(x ** 2) - (y ** 2) 
	return a, b

_signature = inspect.Signature.from_callable(objfunc)

step = 0.1

# state = [old_input, old_output, old_input_rewards, old_output_rewards]
state = [_signature.bind(0.0, 0.0), (0.0, 0.0), (float('-inf'), float('-inf')), (float('-inf'), float('-inf'))]
# where:
# old_input is a BoundArguments
# old_output is either a tuple or a dict. why? because it is not feasible to expect the user to return 
# old_input_rewards is same type as old_input
# old_output_rewards is same type as old_output

input_history         : MutableSequence[BoundArguments]              = [(0.0, 0.0)]
input_rewards_history : MutableSequence[BoundArguments]              = [(0.0, 0.0)]
output_history        : MutableSequence[tuple[...] | dict[str, ...]] = [(0.0, 0.0)]
output_rewards_history: MutableSequence[tuple[...] | dict[str, ...]] = [(0.0, 0.0)]

pareto_front: set[tuple[BoundArguments, ]] = 

for _ in range(1000):
	input_old, output_old = state
	
	# craft new input
	new_input_args: tuple[...] = (val_old + _random.choice((-step, step)) for val_old in input_old)
	new_input_kwargs: dict[str, ...] = {name: val_old + _random.choice((-step, step)) for val_old in input_old}
	 
	# craft new output
	new_output = objfunc(*input_new_args, **input_new_kwargs)
	
	# craft new rewards
	
	y = myfunc(x)
	y_new = myfunc(x_new)
	
	if is_better(y, y_new):
		x = x_new

print(x)

from collections.abc import Callable as _Callable, Sequence as _Sequence
from collections.abc import MutableSequence as _MutableSequence	# for GreedyLocalSearch.default_state
from collections import OrderedDict as _OrderedDict
from inspect import Signature as _Signature, BoundArguments as _BoundArguments
from abc import abstractmethod as _abstractmethod
import random as _random

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
	
	@_abstractmethod
	@property
	def default_state(self) -> any:
		'the state object that the caller should remember so that the optimizer is stateful'
		...
	
	@_abstractmethod
	def optimize(self,
			*,
			state: any,
			pareto_front: None | set[tuple[_BoundArguments, Sequence[any]]] = None,
			) -> set[tuple[_BoundArguments, Sequence[any]]]:
		...

	__call__ = optimize

class GreedyLocalSearch(ParameterOptimizerStrategy):
	@property
	def default_state(self) -> tuple[_BoundArguments[float], _MutableSequence[float]]:
		return ([], [])
	
	def optimize(self, 
			iterations: int,
			step: int,
			*, 
			state: [_MutableSequence[float], _MutableSequence[float]],
			pareto_front: None | set[tuple[_BoundArguments, Sequence[any]]] = None
			) -> set[tuple[_BoundArguments, Sequence[any]]]:

		if pareto_front is None:
			pareto_front = set()

		for _ in range(iterations):
			x_new: _BoundArguments = (state[0] + _random.uniform(-step, step) for param in self.parameters)
			y_new: _Sequence[float] = [self.objective(x_new)]
			
			if any(comparer(y, y_new) for comparer in self.comparers):
				point = x_new, y_new
				state = point
				pareto_front.add(point)

		return pareto_front

class ParameterOptimizer(Optimizer):
	def __init__(self, strategy: ParameterOptimizerStrategy):
		self._strategy: ParameterOptimizerStrategy = strategy
	
	def default_state(self) -> any:
		return self._strategy.default_state
	
	def optimize(self, *args, state: any, pareto_front: None | set[tuple[_BoundArguments, Sequence[any]]] = None, **kwargs) -> set[tuple[_BoundArguments, Sequence[any]]]:
		return self._strategy.optimize(*args, state = state, pareto_front = pareto_front, **kwargs)

	__call__ = optimize
	
paramoptim = GreedyLocalSearch(myfunc, [is_better])
state = paramoptim.default_state
result = paramoptim.optimize(iterations = 1000, step = 0.1, state = state)
print(result)

# NOTE: using Sequence[Callable[[...], bool] for the comparers assumes that the objective function will return the objectives as a tuple. it might not always, so find a cleaner abstraction for this.
# NOTE: likewise, using set[tuple[_BoundArgument, Sequence[any]]] for the pareto front also assumes that the objective returns objectives as a tuple
# stupid. the objectives could even come out as a dict! dont assume. please reabstract this.
