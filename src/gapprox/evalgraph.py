# now.. just think. what is the use of compile when the compiled function cant even take any arguments? it evaluates to the same value every time. the evaluate function should take arguments for the evaluation, and thus the compiled function can also be actually useful. design this later

from __future__ import annotations	# since EvalNode and EvalEdge depend on each other tightly
from .graph import Node, Edge
from typing import Any
import ast	# for ast.NodeVisitor
from numbers import Number	# for typehinting
from collections.abc import Mapping

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
		
		if not target.inputs:
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
				new_edges[edge] = None
		
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

	def evaluate(self, *, memo: None | dict['EvalNode', Any] = None) -> Any:
		memo: dict['EvalNode', Any] = {} if memo is None else memo
		
		if self in memo:
			return memo[self]	# termination
			
		if not self.inputs:
			result = self.payload
		else:
			args: dict[int, Any] = {}
			kwargs: dict[str, Any] = {}
			
			for edge in self.inputs:
				position = edge.position
				value = edge.source.evaluate(memo = memo)	# recursion
			
				match position:
					case int(): 
						if position in args:
							raise ValueError(f'duplicate position [{position}]')
						args[position] = value
					case str(): 
						if position in kwargs:
							raise ValueError(f'duplicate position {position!r}')
						kwargs[position] = value
					case _: 
						raise TypeError(f'{position} is not int or str')
		
			arg_count = len(args)
				# check args continuity
			if not all(index in args for index in range(arg_count)):
				raise ValueError('int position must be contiguous starting from 0')
		
			args: Generator[Any, None, None] = (args[index] for index in range(arg_count))
		
			result = self.payload(*args, **kwargs)
		
		memo[self] = result
		return result
	
	__call__ = evaluate

	def compile() -> Callable:
		...

	@classmethod
	def from_str(cls, string: str, *, translate_dict: dict[ast.AST, Any]) -> 'EvalNode':
		ast_visitor = EvalASTVisitor(translate_dict = translate_dict)
		ast_tree: ast.AST = parse(expr, mode='eval').body
		
		return ast_visitor.visit(ast_tree)
	
	def __repr__(self) -> str:
		return f'<{self.__class__.__name__} at {hex(id(self))}: {len(self.inputs)} inputs, payload={self.payload!r}>'

class EvalEdge(Edge):
	def __init__(self, source: EvalNode, target: EvalNode, position: int | str) -> None:
		if isinstance(position, int) and position < 0:
			raise ValueError('int position must be ≥ 0')
		if not isinstance(position, (int, str)):
			raise TypeError('position must be int or str')
		
		self.position: int | str = position
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
