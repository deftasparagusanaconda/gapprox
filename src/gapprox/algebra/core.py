# ExprNode allows either ExprNode or Symbol for binary operations
# Symbol allows either ExprNode or Symbol for binary operations 

from __future__ import annotations  # defer typehint evaluations to later, all these classes depend on each other
from ..evalgraph import EvalNode, EvalEdge
from .dicts import default_evaluate_dict, default_parse_dict, default_translate_dict
from .symbol import Symbol
import ast
from collections.abc import Iterable
from typing import Any
import operator

#default_parse_dict: Mapping[str, Symbol] = {dunder.strip('_'): default_parse_dict[dunder.strip('_')] for dunder in (operator.__dir__())}

class Symbol:
	'a Symbol encodes meaning, like encoding the meaning of pi, instead of just the value'
	
	def __init__(self, *args, **kwargs):
		self.args: tuple[Any, ...] = args
		self.kwargs: dict[str, Any] = kwargs 

	def __repr__(self) -> str:
		return f"<Symbol at {hex(id(self))}: args={self.args}, kwargs={self.kwargs}>"
	
	def __add__(self, other) -> ExprNode:
		top_node = ExprNode('__add__')
		ExprEdge(self, top_node, 0)
		ExprEdge(other, top_node, 1)
		return top_node

class ExprNode(EvalNode):
	'a node of an expression tree/DAG (directed acyclic graph). it holds an instance of a Symbol as payload'
	


	"""
	_dunder_mapping: Mapping[str, Symbol] = {
		# '__abs__'      : default_parse_dict['abs'     ]
		'__pos__'      : default_parse_dict['pos'     ]
		,'__neg__'      : default_parse_dict['neg'     ]
		,'__add__'      : default_parse_dict['add'     ]
		,'__radd__'     : default_parse_dict['add'     ]
		,'__sub__'      : default_parse_dict['sub'     ]
		,'__rsub__'     : default_parse_dict['sub'     ]
		,'__mul__'      : default_parse_dict['mul'     ]
		,'__rmul__'     : default_parse_dict['mul'     ]
		,'__truediv__'  : default_parse_dict['div'     ]
		,'__rtruediv__' : default_parse_dict['div'     ]
		,'__pow__'      : default_parse_dict['pow'     ]
		,'__rpow__'     : default_parse_dict['pow'     ]
		,'__floordiv__' : default_parse_dict['floordiv']
		,'__rfloordiv__': default_parse_dict['floordiv']
		,'__mod__'      : default_parse_dict['mod'     ]
		,'__rmod__'     : default_parse_dict['mod'     ]
		,'__divmod__'   : default_parse_dict['divmod'  ]
		,'__rdivmod__'  : default_parse_dict['divmod'  ]
		,'__lt__'       : default_parse_dict['lt'      ]
		,'__le__'       : default_parse_dict['le'      ]
		,'__eq__'       : default_parse_dict['eq'      ]
		,'__ne__'       : default_parse_dict['ne'      ]
		,'__ge__'       : default_parse_dict['ge'      ]
		,'__gt__'       : default_parse_dict['gt'      ]
		,'__floor__'    : default_parse_dict['floor'   ]
		,'__round__'    : default_parse_dict['round'   ]
		,'__ceil__'     : default_parse_dict['ceil'    ]
		,'__trunc__'    : default_parse_dict['trunc'   ]
		,'__invert__'   : default_parse_dict['invert'  ]
		,'__and__'      : default_parse_dict['and'     ]
		,'__rand__'     : default_parse_dict['and'     ]
		,'__or__'       : default_parse_dict['or'      ]
		,'__ror__'      : default_parse_dict['or'      ]
		,'__xor__'      : default_parse_dict['xor'     ]
		,'__rxor__'     : default_parse_dict['xor'     ]
		,'__lshift__'   : default_parse_dict['lshift'  ]
		,'__rlshift__'  : default_parse_dict['lshift'  ]
		,'__rshift__'   : default_parse_dict['rshift'  ]
		,'__rrshift__'  : default_parse_dict['rshift'  ]
		,'__bool__'     : default_parse_dict['bool'    ]
		,'__int__'      : default_parse_dict['int'     ]
		,'__str__'      : default_parse_dict['str'     ]
		,'__float__'    : default_parse_dict['float'   ]
		,'__complex__'  : default_parse_dict['complex' ]
	}
	"""

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

class ExprEdge(EvalEdge):
	def __init__(self, source: ExprNode, target: ExprNode, position: int):
		if not isinstance(position, int):
			raise TypeError('position must be int')
		super().__init__(source, target, position)

