from abc import ABC as _ABC
from collections.abc import Callable as _Callable, Sequence as _Sequence
from collections.abc import MutableSequence as _MutableSequence	# for GreedyLocalSearch.default_history
from inspect import Signature as _Signature, BoundArguments as _BoundArguments, Parameter as _Parameter	# for parameters
from abc import abstractmethod as _abstractmethod
import random as _random
from typing import Any as _Any
from collections import deque as _deque, namedtuple as _namedtuple	# for history objects
from .objective import Objective as _Objective

HistoryTuple: _namedtuple = _namedtuple('HistoryTuple', ['inputs', 'input_rewards', 'outputs', 'output_rewards'])

class Optimizer(_ABC):
	'abstract base class for iterative optimization'

class StructureOptimizer(Optimizer):
	...

class ParameterOptimizerStrategy:
	"the optimizer assumes that any exposed parameter on the objective function is available for optimization, exactly as it should assume. after all, its in the name. 'parameter'"
	def __init__(self, objective: _Objective):
		if not isinstance(objective, _Objective):
			raise TypeError(f'{objective} should be an instance of Objective')
		self.objective: _Objective = objective
		
	def get_default_history(
			self, 
			maxlen: int,
			*, 
			default_input_value        : _Any = 0.0, 
			default_output_value       : _Any = 0.0, 
			default_input_reward_value : _Any = float('-inf'),
			default_output_reward_value: _Any = float('-inf'),
			) -> HistoryTuple[
					_deque[tuple[_Any, ...], ...], 
					_deque[tuple[_Any, ...], ...], 
					_deque[tuple[float, ...], ...], 
					_deque[tuple[float, ...], ...]]:
		'create a history object that will store important points. the algorithm may use at most two... lol but this abstraction allows us to have algorithms of any order'
		
		input_count : int = len(self.objective.input_rewarders)
		output_count: int = len(self.objective.output_rewarders)
		
		inputs        : _deque[tuple[_Any, ...], ...]  = _deque([tuple(default_input_value         for _ in range( input_count))] * maxlen, maxlen = maxlen)
		outputs 	  : _deque[tuple[_Any, ...], ...]  = _deque([tuple(default_output_value        for _ in range(output_count))] * maxlen, maxlen = maxlen)
		input_rewards :	_deque[tuple[float, ...], ...] = _deque([tuple(default_input_reward_value  for _ in range( input_count))] * maxlen, maxlen = maxlen)
		output_rewards:	_deque[tuple[float, ...], ...] = _deque([tuple(default_output_reward_value for _ in range(output_count))] * maxlen, maxlen = maxlen)
		
		return HistoryTuple(inputs, outputs, input_rewards, output_rewards)
	
	@staticmethod
	def _update_pareto_front(pareto_front: set[HistoryTuple], new_point: HistoryTuple) -> bool:
		'add a point to a pareto front if it is eligible. if it is eligible, the point is added and it also removes other points on the set that would thus no longer be eligible. returns True if pareto_front was mutated. False if not'
		new_point_inputs, new_point_outputs, new_point_input_rewards, new_point_output_rewards = new_point

		for point in pareto_front:
			point_inputs, point_outputs, point_input_rewards, point_output_rewards = point

			# check if any existing points dominate the new point
			if all(reward >= new_reward for reward, new_reward in zip(point_output_rewards, new_point_output_rewards)) and all(reward >= new_reward for reward, new_reward in zip(point_input_rewards, new_point_input_rewards)) and (any(reward > new_reward for reward, new_reward in zip(point_output_rewards, new_point_output_rewards)) or any(reward > new_reward for reward, new_reward in zip(point_input_rewards, new_point_input_rewards))):
				# new_point is dominated. not eligible. early function termination
				return False
		
		# NOTE: we have two separate loops is because the first loop checks through all possible early terminations first

		dominated: set[HistoryTuple] = set()

		for point in pareto_front:
    	    # check if candidate dominates existing
			if all(new_reward >= reward for new_reward, reward in zip(new_point_output_rewards, point_output_rewards)) and all(new_reward >= reward for new_reward, reward in zip(new_point_input_rewards, point_input_rewards)) and (any(new_reward > reward for new_reward, reward in zip(new_point_output_rewards, point_output_rewards)) or any(new_reward > reward for new_reward, reward in zip(new_point_input_rewards, point_input_rewards))):
				# point is dominated. mark for removal
				dominated.add(point)

		# remove newly dominated points from pareto_front
		pareto_front -= dominated
		
		# add new_point to pareto_front
		pareto_front.add(new_point)

		return True
		
	@_abstractmethod
	def optimize(self,
			*,
			history: _Any,
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		...
	
	__call__ = optimize

class GreedyLocalSearch(ParameterOptimizerStrategy):
	def get_default_history(self, *args, **kwargs):
		return super().get_default_history(maxlen = 1, *args, **kwargs)
	
	def optimize(self, 
			iterations: int,
			step: float,
			*, 
			history: HistoryTuple[_deque, _deque, _deque, _deque],
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		
		pareto_front: set = set() if pareto_front is None else pareto_front
		
		for _ in range(iterations):
			old_inputs, old_outputs, old_input_rewards, old_output_rewards = history

			new_inputs         = tuple(old_input + _random.uniform(-step, step) for old_input in old_inputs[0])
			new_outputs        = self.objective(*new_inputs)
			new_input_rewards  = _Objective.evaluate_rewards(new_inputs, self.objective.input_rewarders)
			new_output_rewards = _Objective.evaluate_rewards(new_outputs, self.objective.output_rewarders)
			
			new_point = HistoryTuple(new_inputs, new_outputs, new_input_rewards, new_output_rewards)
			
			if ParameterOptimizerStrategy._update_pareto_front(pareto_front, new_point):
				old_inputs.appendleft(new_inputs)
				old_outputs.appendleft(new_outputs)
				old_input_rewards.appendleft(new_input_rewards)
				old_output_rewards.appendleft(new_output_rewards)
		
		return pareto_front

class ParameterOptimizer(Optimizer):
	def __init__(self, strategy: ParameterOptimizerStrategy):
		self._strategy: ParameterOptimizerStrategy = strategy
	
	def get_default_history(self, *args, **kwargs) -> _Any:
		return self._strategy.get_default_history(*args, **kwargs)
	
	def optimize(self, 
			*args, 
			history: _Any, 
			pareto_front: None | set[tuple[_BoundArguments, _Sequence[_Any]]] = None,
			**kwargs
			) -> set[tuple[_BoundArguments, _Sequence[_Any]]]:
		return self._strategy.optimize(*args, history = history, pareto_front = pareto_front, **kwargs)

	@classmethod
	def from_GreedyLocalSearch(cls, *args, **kwargs):
		return cls(GreedyLocalSearch(*args, **kwargs))

	__call__ = optimize
