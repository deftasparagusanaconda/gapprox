# strictly speaking, the DAG should not specialize for these things, like specializing InputNode to have different substitution behaviour depending on if payload is a Symbol, or which subclass of Symbol

# for example, in something like ex² + 3.5:
# e is a constant, with a name and a value
# x is a variable, with only a name
# ² and 3.5 are parameters, with only values
# they are all symbols. so thats why i subclass them like this

from typing import Callable, Iterable
from abc import ABC

DEFAULT_PARAMETER_METADATA = {
		'frozen'         : False,
		'mutation_chance': 1.0,
		'mutation_amount': 1.0,
		'tendency'       : None
}

class Symbol(ABC):
	'base class for Variable, Parameter, Constant'
	def __init__(self, name:str, value:any):
		self.name:str = name
		self.value:any = value
		
	def __repr__(self):
		id_str = f"ID={hex(id(self))}"
		name_str = f"name={self.name}"
		value_str = f"value={self.value}"
		type_str = self.__class__.__name__
		return f"<{type_str}: {id_str}, {name_str}, {value_str}>"
		
class Variable(Symbol):
	"""a symbol that represents something that is not supposed to be fixed, and is substituted everytime a function is evaluated. in an equation/function, it is the most volatile kind of symbol

	in an expression like sin(𝑥), we do not typically associate 𝑥 with any particular value. it is dynamically given a value, or a range of values we are interested in. thus Variable only has .name (the '𝑥') but no .value

	the iterative optimization engine will make no attempt at assigning values to variables unless explicitly told to.
	"""
	def __init__(self, name:str):
		super().__init__(name, None)


class Parameter(Symbol):
	"""a symbol that represents something that is supposed to be fixed, but can change across different versions of a function. in an equation/function, it is less volatile than a variable but more volatile than a constant

	in an expression like 2𝑥² + 3𝑥 + 4, the parameters 2, 3, 4 do not typically have a designated name. their value is their name directly. thus Parameter only has .value but no .name

	parameters are the main things the iterative optimization engine changes, besides the expression structure as well. 
	"""
	def __init__(
			self, 
			value: any, 
			name: str = None,
			constraints: Iterable[Callable[[any], bool]] = None,
			metadata: dict = None
			):
		super().__init__(name, value)
		self.constraints: Iterable[Callable[[any], bool]] = set() if constraints is None else constraints
		self.metadata: dict = DEFAULT_PARAMETER_METADATA.copy() if metadata is None else metadata

	def satisfies_constraints(self):
		'check if all constraints are satisfied'
		return all(func(self.value) for func in self.constraints)

	def __repr__(self):
		id_str = f"ID={hex(id(self))}"
		name_str = f"name={self.name}"
		value_str = f"value={self.value}"
		type_str = self.__class__.__name__
		return f"<{type_str}: {id_str}, {name_str}, {value_str}>"

	class Constraints:
		'a collection of constraint functions, for use in Parameter().constraints'
		@staticmethod
		def min(number): return lambda x: x >= number

		@staticmethod
		def max(number): return lambda x: x <= number

		@staticmethod
		def positive():
			from math import copysign
			return lambda x: copysign(1, x) == 1

		@staticmethod
		def negative():
			from math import copysign
			return lambda x: copysign(1, x) == -1

		@staticmethod
		def is_instance(type):
			return lambda x: isinstance(x, type)

class Constant(Symbol):
	"""a symbol that represents something that is supposed to be fixed, and should not change across different versions of a function. in an equation/function, it is the least volatile kind of symbol

	in an expression like sin(𝜋𝑥), we do not typically write the value of 𝜋. instead we write it using its name, and we all agree on its associated value. thus Constant has both .name and .value

	Constant is special in that when it is assigned special values like those in gapprox.constant_dicts, they can participate in algebraic and symbolic manipulation like simplification or formulae (like trig formulae involving 𝜋)

	the iterative optimization engine will not mutate or reassign a Constant, unless explicitly told to.
	"""
