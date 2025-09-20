from .expression import Expression
from typing import Iterable

class Mapping:
	'represents a relational mapping from one thing to another. it can either store a simple dict, or a callable, whose input/output shape represents the mapping'
	def __init__(
			self,
			mapping: dict[any, set[any]] | Expression, 
			input_order:Iterable[str] | None = None):
		if isinstance(mapping, dict):
			if input_order is not None:
				raise TypeError("give either a dict or an Expression and an Iterable[str]")
			self.mapping: dict = mapping
		elif isinstance(mapping, Expression):
			if input_order is None:
				raise TypeError("give either a dict or an Expression and an Iterable[str]")
			self.mapping: Expression = mapping
		
		self.input_order: Iterable[str] | None = input_order

	def get_domain(domain: any) -> any:
		raise NotImplementedError
	
	def get_codomain(domain: any) -> any:
		if isinstance(self.mapping, dict) and domain in self.mapping:
			return self.mapping[domain]

		elif isinstance(self.mapping, Expression):
			kwargs: dict[str, any] = {k: v for k, v in zip(self.input_order, domain)}
			return (self.expression(**kwargs))
	
	__call__ = get_codomain

	def __repr__(self) -> str:
		return f"<Mapping at {hex(id(self))}: mapping=,>"
	
	def __str__(self) -> str:
		output = f"Mapping at {hex(id(self))}"
		output += f"\n    mapping: {type(mapping)}"
		if self.input_order is None:
			output += f"\n    input_order: {self.input_order}"
		else:
			output += f"\n    input_order: {type(self.mapping)}"
		
		return output
			
