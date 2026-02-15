# a wrapper around a function to give it metadata about how to optimize its inputs and outputs

#from inspect import Signature as _Signature
from typing import Any as _Any
from inspect import BoundArguments as _BoundArguments
from collections.abc import Callable as _Callable

class Objective:
	'an objective is a function with instructions that tell us how to optimize it. each input and output is given a reward, and the rewarders are functions that tell us the reward for a given value.'

	def __init__(
			self, 
			function        : _Callable[[...], _Any], 
			input_rewarders : tuple[_Callable[[...], float], ...],
			output_rewarders: tuple[_Callable[[...], float], ...],
			):
		self.function         = function
		self.input_rewarders  = input_rewarders
		self.output_rewarders = output_rewarders
	
	@staticmethod
	def evaluate_rewards(values: tuple[...], rewarders: tuple[_Callable[[...], float]]) -> tuple[float, ...]:
		'return a tuple of rewards for each value, determined by the rewarders'
		return tuple(rewarder(value) for rewarder, value in zip(rewarders, values, strict = True))
	
	# function() = objective()
	def __call__(self, *args, **kwargs) -> _Any:
		return self.function(*args, **kwargs)

	def __repr__(self) -> str:
		return f"<Objective at {hex(id(self))}: >"
