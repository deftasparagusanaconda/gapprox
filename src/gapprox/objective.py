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
			input_rewarders : tuple[Callable[[...], float]] | dict[str, Callable[[...], float]] | _BoundArguments,
			output_rewarders: tuple[Callable[[...], float]] | dict[str, Callable[[...], float]] | _BoundArguments,
			):
		"the shape of input_rewarders and output_rewards implicitly define the shape of the function's input and output"
		self.function         = function
		self.input_rewarders  = input_rewarders
		self.output_rewarders = output_rewarders
	
	@staticmethod
	def evaluate_rewards(
			values   : tuple[...]                    | dict[str, ...]                    | _BoundArguments, 
			rewarders: tuple[Callable[[...], float]] | dict[str, Callable[[...], float]] | _BoundArguments,
			) ->       tuple[float, ...]             | dict[str, float]                  | _BoundArguments:
		'call the rewarders on the values and return their same type'
		assert type(values) == type(rewarders)	# yes, an *exact* type equality, not subclassed equality

		match values:
			case tuple():
				return tuple(rewarder(value) for rewarder, value in zip(rewarders, values, strict = True))

			case dict():
				assert len(values) == len(rewarders)
				return {name: rewarder(values[name]) for name, rewarder in rewarders.items()}

			case _BoundArguments():
				assert values.signature == rewarders.signature
				args = (rewarder(value) for rewarder, value in zip(rewarders.args, values.args, strict = True))
				kwargs = {name: rewarder(values.kwargs[name]) for name, rewarder in rewarders.kwargs.items()}
				return values.signature.bind(*args, **kwargs)

			case _:
				raise ValueError('values should be tuple or dict or BoundArguments')
	
	# function() = objective()
	def __call__(*args, **kwargs) -> _Any:
		return self.function(*args, **kwargs)

	def __repr__(self) -> str:
		return f"<Objective at {hex(id(self))}: >"
