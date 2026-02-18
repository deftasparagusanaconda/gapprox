# ExprNode allows either ExprNode or Symbol for binary operations
# Symbol allows either ExprNode or Symbol for binary operations 

from __future__ import annotations  # defer typehint evaluations to later, all these classes depend on each other
from ..evalgraph import EvalNode, EvalEdge
from .dicts import default_evaluate_dict, default_parse_dict, default_translate_dict
from .symbol import Symbol
import ast
from collections.abc import Iterable
from typing import Any

class Symbol:
	'a Symbol encodes meaning, like encoding the meaning of pi, instead of just the value'
	
	def __init__(self, name: str):
		self.name: str = name

	def __repr__(self) -> str:
		return f"<Symbol at {hex(id(self))}: name = {self.name}>"
	
#	def __add__(self, other) -> ExprNode:	

class ExprNode(EvalNode):
	'a node of an expression tree/DAG (directed acyclic graph). it holds an instance of a Symbol as payload'
	
	def __init__(self, payload: Symbol):
		if not isinstance(payload, Symbol):
			raise TypeError('payload must be Symbol')
		super().__init__(payload)
		
	#@classmethod
	#def from_any(cls, thing: Any) -> None:
	#    return thing if isinstance(thing, cls) else cls(thing)
	
	def to_EvalNode(
			self                                                     ,
			substitutions        : None | dict[Symbol  , Any] = None ,
			*                                                        ,
			default_substitutions: None | dict[Symbol  , Any] = None ,
			memo                 : None | dict[EvalNode, Any] = None ,
			substitute_payload   : bool                       = False,
			) -> Any:
		substitutions = {} if substitutions is None else substitutions
		default_substitutions: dict[Symbol, Any] = default_evaluate_dict if default_substitutions is None else default_substitutions
		memo: dict[EvalNode, Any] = {} if memo is None else memo

		if self in memo:
			return memo[self]   # termination

		# substitutions overrides default_substitutions
		substitutions = default_substitutions | substitutions
		
		payload = substitutions.get(self.payload, self.payload)
		
		if not self.inputs: 
			result = payload
		else:
			positions: set[int] = {edge.position for edge in self.inputs}
			input_count: int = len(self.inputs)
			
			if len(positions) != input_count:
				raise ValueError('duplicate indices found')

			if positions != set(range(input_count)):
				raise ValueError('index must be contiguous starting from 0')
				
			args: list[Any] = [None] * input_count
			
			for edge in self.inputs:
				args[edge.position] = edge.source.evaluate(
						substitutions = substitutions, 
						default_substitutions = {}, 
						memo = memo)   # recursion
			
			result = payload(*args)

		memo[self] = result
		return result

	def evaluate(*args, **kwargs) -> Any:
		return self.to_EvalNode.evaluate(*args, **kwargs)
	
	def __add__(self, other) -> ExprNode:
		if not isinstance(other, ExprNode):
			raise TypeError('can only add ExprNode and ExprNode')
		payload: Callable[[Any, Any], Any] = type(self)._parse_dict['__add__']
	
	def __neg__(self) -> ExprNode:
		return ExprNode

class ExprEdge(EvalEdge):
	def __init__(self, source: ExprNode, target: ExprNode, position: int):
		if not isinstance(position, int):
			raise TypeError('position must be int')
		super().__init__(source, target, position)

