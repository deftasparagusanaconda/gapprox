# now.. just think. what is the use of compile when the compiled function cant even take any arguments? it evaluates to the same value every time. the evaluate function should take arguments for the evaluation, and thus the compiled function can also be actually useful. design this later

from __future__ import annotations	# since EvalNode and EvalEdge depend on each other tightly
from .graph import Node, Edge
from typing import Any
import ast	# for ast.NodeVisitor
from numbers import Number	# for typehinting
from collections.abc import Mapping

import operator, math, builtins	# for dunders

class EvalNode(Node):

	def __init__(self, payload: Any) -> None:
		self.payload: Any = payload
		super().__init__()

	def substitute(
			self, 
			node_substitutions: None | Mapping[EvalNode | Any, EvalNode | Any] = None,
			edge_substitutions: None | Mapping[EvalEdge | int | str, int | str] = None,
			*, 
			payload_first: bool = False,
		) -> EvalNode:
		"""recursively replace nodes and edges by first checking node identity, then payload identity. the precedence of node identity and payload identity can be reversed with the boolean payload_first parameter (default is False).

		the original graph is not mutated. duplicates are created only where necessary. if a branch was unchanged, it is not duplicated. if any edge or node is duplicated, everything above it is also duplicated. (the root node is often duplicated whereas the leaf nodes are often not)

		if a node/edge is substituted with a new payload, a new node/edge is created. everything from the root to itself is also duplicated.
		if a node is substituted with a new node, it is considered a graft, and is not recursed further. 
		an edge cannot be substituted with a new edge, because the graph would have to create a new target node, which the new edge would not be aware of. (this would have been possible if .substitute is mutating, but it is not)
		"""
		# initialize node_substitutions and edge_substitutions
		node_substitutions: Mapping[EvalNode | Any, EvalNode | Any] = dict() if node_substitutions is None else node_substitutions
		edge_substitutions: Mapping[EvalEdge | int | str, EvalNode | int | str] = dict() if edge_substitutions is None else edge_substitutions
	
		# we call the current node 'target', in relation to the potentially new edges we might construct later
		target: EvalNode = self

		# look up node in node_substitutions
		keys = (self.payload, self) if payload_first else (self, self.payload)
		for key in keys:
			if key not in node_substitutions:
				continue
			
			val = node_substitutions[key]
			
			if isinstance(val, EvalNode):
				# we encounter a {node | payload: node} substitution. these are simply grafted as-is, and not recursed
				return val	# termination
			else:
				# we encounter a {node | payload: payload} substitution. we wrap the payload in a new node, and recurse
				target = EvalNode(val)	# instantiation
				break
		
		if not self.inputs:
			return target	# termination
		
		# create a handy dandy dict of {old_edge: new_payload}
		'''
		new_edges: dict[EvalEdge, EvalEdge] = {
			edge: 
			edge_substitutions.get(
				first_key 
				if first_key in edge_substitutions 
				else second_key
				, edge) 
			for edge 
				in self.inputs
			for first_key, second_key
				in (
					(edge.payload, edge) 
					if payload_first 
					else (edge, edge.payload)
			)
		}
		'''

		# this comprehension version was just a joke xd heres the real readable version:
		
		new_edges: dict[EvalEdge, EvalEdge] = dict()
		for edge in self.inputs:
			# look up edge in edge_substitutions
			first_key, second_key = (edge.payload, edge) if payload_first else (edge, edge.payload)

			#new_edges[edge] = edge_substitutions.get(first_key if first_key in edge_substitutions else second_key, edge)
			if first_key in edge_substitutions:
				new_edges[edge] = edge_substitutions[first_key]
			elif second_key in edge_substitutions:
				new_edges[edge] = edge_substitutions[second_key]
			else:
				new_edges[edge] = edge.payload
		
		# new_edges now looks like {e1: None, e2: 2, e3: my_edge, …}
		
		no_edge_changes: bool = all(val is None for val in new_edges.values())
		no_node_changes: bool = target is self
		if no_edge_changes and no_node_changes:
			return self	# termination
		
		# now we know new_edges definitely has at least one substitution ready >:)
		# so target cant be self anymore. if target is still self, we need to make it a duplicate
		target = EvalNode(target.payload) if target is self else target	# instantiation
		
		for edge, new_payload in new_edges.items():
			if not isinstance(new_payload, (int, str)):
				raise TypeError('edge_substitutions values can only be int or str')
			source = edge.source.substitute(node_substitutions,edge_substitutions, payload_first = payload_first)	# recursion
			EvalEdge(source, target, new_payload)	# instantiation
		
		return target
		
	def _evaluate_without_arguments(self, *, memo: None | dict['EvalNode', Any] = None) -> Any:
		memo: dict['EvalNode', Any] = {} if memo is None else memo
		
		if self in memo:
			return memo[self]	# termination
			
		if not self.inputs:
			result = self.payload
		else:
			args_dict: dict[int, Any] = {}
			kwargs: dict[str, Any] = {}
			
			for edge in self.inputs:
				payload = edge.payload
				value = edge.source.evaluate(memo = memo)	# recursion
			
				match payload:
					case int(): 
						if payload in args_dict:
							raise ValueError(f'duplicate payload [{payload}]')
						args_dict[payload] = value
					case str(): 
						if payload in kwargs:
							raise ValueError(f'duplicate payload {payload!r}')
						kwargs[payload] = value
					case _: 
						raise TypeError(f'{payload} is not int or str')
			
			arg_count = len(args_dict)
				# check args_dict continuity
			if not all(index in args_dict for index in range(arg_count)):
				raise ValueError('int payload must be contiguous starting from 0')
		
			args: Generator[Any, None, None] = (args_dict[index] for index in range(arg_count))
		
			result = self.payload(*args, **kwargs)
		
		memo[self] = result
		return result
	
	def evaluate(self, node_substitutions = None, edge_substitutions = None, *, payload_first = False, memo = None) -> Any:
		return self.substitute(node_substitutions, edge_substitutions, payload_first = payload_first)._evaluate_without_arguments(memo = memo)

	def compile() -> Callable:
		...

	@classmethod
	def from_str(cls, string: str, *, translate_dict: dict[ast.AST, Any]) -> 'EvalNode':
		ast_visitor = EvalASTVisitor(translate_dict = translate_dict)
		ast_tree: ast.AST = parse(expr, mode='eval').body
		
		return ast_visitor.visit(ast_tree)
		
	@staticmethod
	def _dunder_factory(operator: Callable, *, reverse_args: bool = False) -> Callable:
		
		def dunder(*args, **kwargs) -> EvalNode:
			if not (all(isinstance(arg, EvalNode) for arg in args) and all(isinstance(kwarg, EvalNode) for kwarg in kwargs)):
				raise TypeError('only compatible with EvalNode')
			top_node = EvalNode(operator)
			for index, arg in enumerate(reversed(args) if reverse_args else args):
				EvalEdge(arg, top_node, index)
			for key, kwarg in kwargs.items():
				EvalEdge(kwarg, top_node, key)
			return top_node

		return dunder
		
	__lt__        = _dunder_factory(operator.lt                         )	# x < y
	__le__        = _dunder_factory(operator.le                         )	# x <= y
	__eq__        = _dunder_factory(operator.eq                         )	# x == y
	__ne__        = _dunder_factory(operator.ne                         )	# x != y
	__ge__        = _dunder_factory(operator.ge                         )	# x >= y
	__gt__        = _dunder_factory(operator.gt                         )	# x > y

	__abs__       = _dunder_factory(operator.abs                        )	# abs(x)
	__pos__       = _dunder_factory(operator.pos                        )	# +x
	__neg__       = _dunder_factory(operator.neg                        )	# -x
	__add__       = _dunder_factory(operator.add                        )	# x + y
	__radd__      = _dunder_factory(operator.add     , reverse_args=True)	# y + x
	__sub__       = _dunder_factory(operator.sub                        )	# x - y
	__rsub__      = _dunder_factory(operator.sub     , reverse_args=True)	# y - x
	__mul__       = _dunder_factory(operator.mul                        )	# x * y
	__rmul__      = _dunder_factory(operator.mul     , reverse_args=True)	# y * x
	__truediv__   = _dunder_factory(operator.truediv                    )	# x / y
	__rtruediv__  = _dunder_factory(operator.truediv , reverse_args=True)	# y / x
	__pow__       = _dunder_factory(operator.pow                        )	# x ** y
	__rpow__      = _dunder_factory(operator.pow     , reverse_args=True)	# y ** x
	
	__floordiv__  = _dunder_factory(operator.floordiv                   )	# x // y
	__rfloordiv__ = _dunder_factory(operator.floordiv, reverse_args=True)	# x // y
	__mod__       = _dunder_factory(operator.mod                        )	# x % y
	__rmod__      = _dunder_factory(operator.mod     , reverse_args=True)	# y % x
	__divmod__    = _dunder_factory(builtins.divmod                     )	# divmod(x, y)
	__rdivmod__   = _dunder_factory(builtins.divmod  , reverse_args=True)	# divmod(y, x)
	
	__matmul__    = _dunder_factory(operator.matmul                     )	# x @ y
	
	__invert__    = _dunder_factory(operator.invert                     )	# ~x
	__and__       = _dunder_factory(operator.and_                       )	# x & y	
	__rand__      = _dunder_factory(operator.and_    , reverse_args=True)	# y & x
	__or__        = _dunder_factory(operator.or_                        )	# x | y
	__ror__       = _dunder_factory(operator.or_     , reverse_args=True)	# y | x
	__xor__       = _dunder_factory(operator.xor                        )	# x ^ y
	__rxor__      = _dunder_factory(operator.xor     , reverse_args=True)	# y ^ x
	__lshift__    = _dunder_factory(operator.lshift                     )	# x << y
	__rlshift__   = _dunder_factory(operator.lshift  , reverse_args=True)	# y << x
	__rshift__    = _dunder_factory(operator.rshift                     )	# x >> y
	__rrshift__   = _dunder_factory(operator.rshift  , reverse_args=True)	# y >> x

	__round__     = _dunder_factory(builtins.round                      )	# round(x, [y])
	__trunc__     = _dunder_factory(math.trunc                          )	# trunc(x)
	__floor__     = _dunder_factory(math.floor                          )	# floor(x)
	__ceil__      = _dunder_factory(math.ceil                           )	# ceil(x)

	__call__      = _dunder_factory(operator.call                       )	# x(…)
	__getitem__   = _dunder_factory(operator.getitem                    )	# x[y][…]…
	__setitem__   = _dunder_factory(operator.setitem                    )	# x[y][…]… = z
	__delitem__   = _dunder_factory(operator.delitem                    )	# del x[y][…][…]… 

	__enter__      = _dunder_factory(operator.call                       )	# x(…)
	__enter__      = _dunder_factory(operator.call                       )	# x(…)

	# do NOT define these because the corresponding dunder expects the corresponding type to be returned, not EvalNode
	#__bool__      = _dunder_factory(bool                                )	# bool(x)
	#__int__       = _dunder_factory(int                                 )	# int(x)
	#__float__     = _dunder_factory(float                               )	# float(x)
	#__complex__   = _dunder_factory(complex                             )	# complex(x)
	#__str__       = _dunder_factory(str                                 )	# str(x)

	# NOTE: why dont we implicitly wrap non-EvalNode operands to EvalNode? because:
	# 
	# imagine this scenario. you have `x = EvalNode('x')`. if we allowed implicit wrapping:
	# 2 + 4 + x would create this tree:
	#
	#   + 
	#  / \
	# 6   x
	#
	# this is because the other parts of the expression that are not EvalNode will evaluate to a single value. if we disallow implicit wrapping, we are forced to do:
	# EvalNode(2) + EvalNode(4) + x which would correctly create the tree:
	#
	#     +    
	#    / \      
	#   +   x 
	#  / \       
	# 2   4    
	# 
	# thus we protect the user from any unexpected behaviour. it is less convenient but it is more important to be correct, in our case. gapprox is not mainly a convenience tool. robustness first. in fact, if you want such convenience, youre probably better off using ExprNode.from_str
	
	# because we defined __eq__, __hash__ needs to be set manually
	#def __hash__(self):
	#	return id(self)
	__hash__ = object.__hash__

	def __repr__(self) -> str:
		return f'<{self.__class__.__name__} at {hex(id(self))}: {len(self.inputs)} inputs, payload={self.payload!r}>'

class EvalEdge(Edge):
	def __init__(self, source: EvalNode, target: EvalNode, payload: int | str) -> None:
		if isinstance(payload, int) and payload < 0:
			raise ValueError('int payload must be ≥ 0')
		if not isinstance(payload, (int, str)):
			raise TypeError('payload must be int or str')
		
		self.payload: int | str = payload
		super().__init__(source, target)

default_translate_dict: dict[ast.AST, Any]

class EvalASTVisitor(ast.NodeVisitor):
	'stateful function that visits ast.AST nodes and creates a graph of EvalNode. use .visit(ast.AST node). it returns the top EvalNode'
	
	def __init__(*, translate_dict: None | dict[ast.AST, Any] = None):
		self.translate_dict: dict[ast.AST, str] = default_translate_dict if translate_dict is None else translate_dict

	def generic_visit(self, node: ast.AST) -> None:
		raise NotImplementedError(f"critical error! {node!r} of type {type(node)!r} is not recognized. please report this")
		
	def visit_Constant(self, node: ast.AST) -> EvalNode:	# a number, like 2 in '2+x'
		return EvalNode(node.value)
	
	def visit_Name(self, node: ast.AST) -> EvalNode:	# any unrecognized string
		return EvalNode(node.id)

	def visit_UnaryOp(self, node: ast.AST) -> EvalNode:
		if type(node.op) not in self.translate_dict:
			raise NotImplementedError(f"{node.op} not supported")
		
		func_expr = EvalNode(self.translate_dict[op])
		operand_expr = self.visit(node.operand)	# recursion
		EvalEdge(expr, func_expr, 0)
		return func_expr

	def visit_BinOp(self, node: ast.AST) -> EvalNode:
		if type(node.op) not in self.translate_dict:
			raise NotImplementedError(f"{node.op} not supported")
		
		func_expr = EvalNode(self.translate_dict[op])
		left = self.visit(node.left)	# recursion
		right = self.visit(node.right)	# recursion
		EvalEdge(left, func_node, 0)
		EvalEdge(right, func_node, 1)
		return func_expr
	
	def visit_Call(self, node: ast.AST) -> EvalNode:
		name = node.func.id
		
		if name not in self.parse_dict:
			raise KeyError(f'{name!r} isnt recognized. check parse_dict')
			
		op: Symbol = self.parse_dict[name]
		args: Generator[EvalNode, None, None] = (self.visit(arg) for arg in node.args)	# recursion
		
		# connect args as inputs to op
		func_node = EvalNode(op)
		for index, arg in enumerate(args):
			EvalEdge(arg, func_node, index)
		
		return func_node

	def visit_Compare(self, node: ast.AST) -> EvalNode:
		'assumes comparison operators are binary operators'
		args: tuple[EvalNode] = tuple(self.visit(arg) for arg in [node.left] + node.comparators)	# recursion

		func_nodes: list[EvalNode] = []
		for index, op in enumerate(node.ops):
			op_type = type(op)
			if op_type not in self.translate_dict:
				raise NotImplementedError(f"{op} not supported")
			func_node = EvalNode(self.translate_dict[op_type])
			EvalEdge(args[index], func_node, 0)
			EvalEdge(args[index+1], func_node, 1)
			func_nodes.append(func_node)

		if len(func_nodes) == 1:  # simple unchained case
			return func_nodes[0]

		# route all to a tuple wrapper
		tuple_funcnode = EvalNode(tuple)
		for index, func_node in enumerate(func_nodes):
			EvalEdge(func_node, tuple_funcnode, index)
		
		# route tuple wrapper to all()
		all_funcnode = EvalNode(all)
		EvalEdge(tuple_funcnode, all_funcnode, 0)
		
		return all_funcnode
	
	def visit_BoolOp(self, node: ast.AST) -> EvalNode:
		'uses AND/OR if binary, ALL/ANY if variadic'
		op = type(node.op)

		if op not in self.translate_dict:
			raise NotImplementedError(f"{node.op} not supported")

		if len(node.values) == 2:	# binary
			func_node = EvalNode(self.translate_dict[op])
			in1 = self.visit(node.values[0])	# recursion
			in2 = self.visit(node.values[1])	# recursion
			EvalEdge(in1, func_node, 0)
			EvalEdge(in2, func_node, 1)
			return func_node

		if isinstance(node.op, ast.And):
			func_node = EvalNode(all)
		elif isinstance(node.op, ast.Or):
			func_node = EvalNode(any)
		else:
			raise ValueError(f"critical error! {node.op} not recognized")
		
		tuple_node = EvalNode(tuple)
		
		for index, value in enumerate(node.values):
			input = self.visit(value)	# recursion
			EvalEdge(input, tuple_node, index)
		
		EvalEdge(tuple_node, func_node, 0)
		
		return func_node
	
	def visit_IfExp(self, node: ast.AST) -> EvalNode:
		"if else expression. ast formats it like: 'node.body if node.test else node.orelse' and gapprox follows a 'a if b else c' order, instead of a 'if a then b else c' order"
		op = type(node)
		
		if op not in self.translate_dict:
			raise NotImplementedError(f"{node.op} not supported")
		
		func_node = EvalNode(self.translate_dict[op])
		
		body_node: EvalNode = self.visit(node.body)	# recursion
		test_node: EvalNode = self.visit(node.test)	# recursion
		orelse_node: EvalNode = self.visit(node.orelse)	#recursion
		
		EvalEdge(body_node, func_node, 0)
		EvalEdge(test_node, func_node, 1)
		EvalEdge(orelse_node, func_node, 2)
		
		return func_node
	
	def visit_Lambda(self, node: ast.AST):
		raise NotImplementedError("the developer is still debating how to represent a lambda function in a DAG. should she represent it as an object? a FunctionNode? an InputNode? its own self-contained Dag? or self-contained Function? these are perplexing questions...")

	def visit_Subscript(self, node: ast.AST):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

	def visit_Attribute(self, node: ast.AST):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")
