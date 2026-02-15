import ast
from .graph import Node, Edge
from .parse_dict import default_parse_dict
from .symbol import Symbol
from numbers import Number
from collections.abc import Iterable
from typing import Any
from .context import default_context

DEFAULT_FUNCTION_PARSE_DICT: dict[str, Symbol] = {key.name: key for key in default_context.keys()}

class AstToMultiDAGVisitor(ast.NodeVisitor):
	'stateful function that adds nodes of an ast to a MultiDAG'
	def __init__(self, symbols_dict: dict[str: Symbol], function_parse_dict: dict[str, Symbol] = DEFAULT_FUNCTION_PARSE_DICT, parse_dict: dict[ast.AST, Symbol] = default_parse_dict):
		self.symbols_dict: dict[str, Symbol] = function_parse_dict.copy()
		self.symbols_dict.update(symbols_dict)	# symbols_dict overrides function_parse_dict
		self.parse_dict: dict[ast.AST, str] = parse_dict

	def generic_visit(self, node: Node) -> None:
		raise NotImplementedError(f"critical error! {node!r} of type {type(node)!r} is not recognized. please report this")
		
	def visit_Constant(self, node: Node) -> Node[Number]:	# a number, like 2 in '2+x'
		return Node(node.value)
	
	def visit_Name(self, node: Node) -> Node[Symbol]:	# any unrecognized string
		if node.id not in self.symbols_dict:
			raise Exception(f'didnt find {node.id} in symbols_dict')
		return Node(self.symbols_dict[node.id])

	def visit_UnaryOp(self, node: Node) -> Node[Symbol]:
		op = type(node.op)
		
		if op not in self.parse_dict:
			raise NotImplementedError(f"{node.op} not supported")
		
		func_node = Node(self.parse_dict[op])
		operand = self.visit(node.operand)	# recursion
		Edge(operand, func_node, 0)
		return func_node

	def visit_BinOp(self, node: Node) -> Node:
		op = type(node.op)
		
		if op not in self.parse_dict:
			raise NotImplementedError(f"{node.op} not supported")
		
		func_node = Node(self.parse_dict[op])
		left = self.visit(node.left)	# recursion
		right = self.visit(node.right)	# recursion
		Edge(left, func_node, 0)
		Edge(right, func_node, 1)
		return func_node
	
	def visit_Call(self, node) -> Node:
		op: Symbol = self.symbols_dict[node.func.id]
		args: list[Node] = [self.visit(arg) for arg in node.args]	# recursion
		
		# connect args as inputs to op
		func_node = Node(op)
		for index, arg in enumerate(args):
			Edge(arg, func_node, index)
		
		return func_node

	def visit_Compare(self, node) -> Node:
		'assumes comparison operators are binary operators'
		args: tuple[Node] = tuple(self.visit(arg) for arg in [node.left] + node.comparators)	# recursion

		func_nodes: list[Node] = []
		for index, op in enumerate(node.ops):
			op_type = type(op)
			if op_type not in self.parse_dict:
				raise NotImplementedError(f"{op} not supported")
			func_node = Node(self.parse_dict[op_type])
			Edge(args[index], func_node, 0)
			Edge(args[index+1], func_node, 1)
			func_nodes.append(func_node)

		if len(func_nodes) == 1:  # simple unchained case
			return func_nodes[0]

		# route all to a tuple wrapper
		tuple_funcnode = Node(tuple)
		for index, func_node in enumerate(func_nodes):
			Edge(func_node, tuple_funcnode, index)
		
		# route tuple wrapper to all()
		all_funcnode = Node(all)
		Edge(tuple_funcnode, all_funcnode, 0)
		
		return all_funcnode
	
	def visit_BoolOp(self, node) -> Node:
		'uses AND/OR if binary, ALL/ANY if variadic'
		op = type(node.op)

		if op not in self.parse_dict:
			raise NotImplementedError(f"{node.op} not supported")

		if len(node.values) == 2:	# binary
			func_node = Node(self.parse_dict[op])
			in1 = self.visit(node.values[0])	# recursion
			in2 = self.visit(node.values[1])	# recursion
			Edge(in1, func_node, 0)
			Edge(in2, func_node, 1)
			return func_node

		if isinstance(node.op, ast.And):
			func_node = Node(all)
		elif isinstance(node.op, ast.Or):
			func_node = Node(any)
		else:
			raise ValueError(f"critical error! {node.op} not recognized")
		
		tuple_node = Node(tuple)
		
		for index, value in enumerate(node.values):
			input = self.visit(value)	# recursion
			Edge(input, tuple_node, index)
		
		Edge(tuple_node, func_node, 0)
		
		return func_node
	
	def visit_IfExp(self, node) -> Node:
		"if else expression. ast formats it like: 'node.body if node.test else node.orelse' and gapprox follows a 'a if b else c' order, instead of a 'if a then b else c' order"
		op = type(node)
		
		if op not in self.parse_dict:
			raise NotImplementedError(f"{node.op} not supported")

		func_node = Node(self.parse_dict[op])
		
		body_node: Node = self.visit(node.body)	# recursion
		test_node: Node = self.visit(node.test)	# recursion
		orelse_node: Node = self.visit(node.orelse)	#recursion
		
		Edge(body_node, func_node, 0)
		Edge(test_node, func_node, 1)
		Edge(orelse_node, func_node, 2)

		return func_node
	
	def visit_Lambda(self, node):
		raise NotImplementedError("the developer is still debating how to represent a lambda function in a DAG. should she represent it as an object? a FunctionNode? an InputNode? its own self-contained Dag? or self-contained Function? these are perplexing questions...")

	def visit_Subscript(self, node):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

	def visit_Attribute(self, node):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")
