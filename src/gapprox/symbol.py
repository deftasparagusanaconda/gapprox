# for example, in something like ex² + 3.5:
# e is a constant, with a name and a value
# x is a variable, with only a name
# ² and 3.5 are parameters, with only values
# they are all symbols. so thats why i subclass them like this

# strictly speaking, the DAG should not specialize for these things, like specializing InputNode to have different substitution behaviour depending on if payload is a Symbol, or which subclass of Symbol, etc

# like most other symbolic systems like sympy, tensorflow, mathematica, etc, gapprox considers Variable to be name first, Parameter to be value first, and Constant to be name first
# a Variable is never assigned a value, but can be assigned one after instantiation
# a Parameter is a value first and foremost, but also optionally has a name
# a Constant makes sense with just a name, even without a value

# something like 3xᵉ + pxᵖ + sin(πy) where p = 2 will look like:
# var1 = Variable('x')
# var2 = Variable('y')
# param1 = Parameter(3)
# param1 = Parameter(2, name='p')
# const1 = Constant('π', value=math.pi)
# const2 = Constant('e', value=math.e)
# param1*var1**const2 + param1*var1**param1 + sin(const1*var2)
# (technically, you should use const1=gapprox.constants.e and const2=gapprox.constants.pi, which are specially supported for algebraic manipulation like simplification)

# ALL attributes of Variable, Parameter, Constant are mutable. changing the name of a Constant does not affect its identity in the expression, because in gapprox, an expression is stored in a Dag, and a Dag only cares about object id, not the name

from typing import Callable, Iterable
from abc import ABC

DEFAULT_PARAMETER_METADATA = {
		'frozen'         : False,
		'mutation_chance': 1.0,
		'mutation_amount': 1.0,
		'value_tendency' : None
}

class Symbol(ABC):
	'base class for Variable, Parameter, Constant'
	def __init__(self, name: str = None, value: any = None):
		if type(self) is Symbol:
			raise TypeError("Symbol is an abstract class. use Variable, Parameter, or Constant")
		self.name: str = name
		self.value: any = value
		
	def __repr__(self):
		name_str = f"name={self.name!r}"
		value_str = f"value={self.value!r}"
		type_str = self.__class__.__name__
		return f"<{type_str} at {hex(id(self))}: {name_str}, {value_str}>"
		
class Variable(Symbol):
	"""a symbol that represents something that is not supposed to be fixed, and is substituted everytime a function is evaluated. in an equation/function, it is the most volatile kind of symbol

	in an expression like sin(𝑥), we do not typically associate 𝑥 with any particular value. it is dynamically given a value, or a range of values we are interested in. thus Variable only has .name (the '𝑥') but no .value

	the iterative optimization engine will make no attempt at assigning values to variables unless explicitly told to.
	"""
	def __init__(self, name:str):
		super().__init__(name=name)

class Parameter(Symbol):
	"""a symbol that represents something that is supposed to be fixed, but can change across different mutations of a function. in an equation/function, it is less volatile than a variable but more volatile than a constant

	in an expression like 2𝑥² + 3𝑥 + 4, the parameters 2, 3, 4 do not typically have a designated name. their value is their name directly. thus Parameter only has .value but no .name

	parameters are the main things the iterative optimization engine changes, besides the expression structure as well. 
	"""
	def __init__(
			self, 
			value: any, 
			*,
			name: str = None,
			constraints: Iterable[Callable[[any], bool]] = None,
			metadata: dict = None
			):
		super().__init__(name=name, value=value)
		self.constraints: Iterable[Callable[[any], bool]] = set() if constraints is None else constraints
		self.metadata: dict = DEFAULT_PARAMETER_METADATA.copy() if metadata is None else metadata

	def satisfies_constraints(self):
		'check if all constraints are satisfied'
		return all(func(self.value) for func in self.constraints)

	def __repr__(self):
		name_str = f"name={self.name!r}"
		value_str = f"value={self.value!r}"
		type_str = self.__class__.__name__
		return f"<{type_str} at {hex(id(self))}: {value_str}, {name_str}>"

	class Constraints:
		'a collection of constraint functions, for use in Parameter().constraints'

		@staticmethod
		def is_less_than(number): return lambda x: x < number

		@staticmethod
		def is_less_than_or_equal_to(number): return lambda x: x <= number

		@staticmethod
		def is_equal_to(number): return lambda x: x == number

		@staticmethod
		def is_not_equal_to(number): return lambda x: x != number

		@staticmethod
		def is_greater_than_or_equal_to(number): return lambda x: x >= number

		@staticmethod
		def is_greater_than(number): return lambda x: x > number

		@staticmethod
		def is_prime(): raise NotImplementedError("prime checking algorithm not yet implemented")
		
		@staticmethod
		def is_composite(): raise NotImplementedError("composite checking algorithm not yet implemented")
		
		@staticmethod
		def is_positive():
			from math import copysign
			return lambda x: copysign(1, x) == 1

		@staticmethod
		def is_negative():
			from math import copysign
			return lambda x: copysign(1, x) == -1

		@staticmethod
		def is_integer(): return lambda x: x % 0 == 0

		@staticmethod
		def is_real(): return lambda x: hasattr(x, 'real')
	
		@staticmethod
		def is_imaginary(): return lambda x: isinstance(x, complex) and x.real == 0

		@staticmethod
		def is_complex(): return lambda x: isinstance(x, complex)
	
		@staticmethod
		def is_instance(thing): return lambda x: isinstance(x, thing)

		@staticmethod
		def is_type(thing): return lambda x: type(x) == thing

class Constant(Symbol):
	"""a symbol that represents something that is supposed to be fixed, and should not change across different versions of a function. in an equation/function, it is the least volatile kind of symbol

	in an expression like sin(π𝑥), we do not typically write the value of π. instead we write it using its name, and we all agree on its associated value. thus Constant has both .name and .value

	Constant is special in that when it is assigned special values like those in gapprox.constant_dicts, they can participate in algebraic and symbolic manipulation like simplification or formulae (like trig formulae involving π)

	the iterative optimization engine will not mutate or reassign a Constant, unless explicitly told to.
	"""
	def __init__(self, name: str, *, value: any = None):
		super().__init__(name=name, value=value)
		self.name: str = name
		self.value: any = value
