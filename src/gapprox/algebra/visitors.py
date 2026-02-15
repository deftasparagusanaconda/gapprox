# we kinda *want* something that can update the inputs list for the operators because inputs lists are being dynamically grown which can get pretty expensive, i think. dynamic allocation is always slower than static allocation

import gapprox
from ..graph import Node

class NodeVisitor:
	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

	base class for any node visitor
	"""
#	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

#	this class is really just a stateful function that traverses through nodes in a DAG. the difference is that it will have different logic for different kinds of nodes. you make a subclass of it, and there you define visit_* methods, where * is your node's class name. say you have ParameterNode. then you would define something like visit_ParameterNode and you would call MyNodeVisitorSubclass().visit(ParameterNode)

#	like ast.NodeVisitor, it defines visit and generic_visit, and subclasses are supposed to define visit_* (* meaning YourClassName)
#	unlike ast.NodeVisitor, it does not define generic_visit or visit_Constant, is not specific to a tree structure, and is not specific to ast nodes. it supports a directed acyclic graph data structure, and is generic to *any* kind of DAG node (i think). it also is not limited to root-to-leaf traversal, and can be bi-directional or such

#	for a tree structure, a node is visited once. for a DAG structure, a node may be visited multiple times. implement your own memoization if you do not want this repeated traversal.

#	to mutate nodes during traversal, use gapprox.NodeTransformer instead. NodeVisitor is only meant for read-only traversal

#	it is generally recommended to name any subclasses of NodeVisitor as *Visitor such as SubstitutionVisitor, StringifyVisitor, …
#	"""

	def visit(self, node) -> any:
		'the thing to call to start traversal. never start traversal by calling visit_*(mynode). always start traversal by calling visit(mynode)'

		method = 'visit_' + str(node.metadata)
		visitor = getattr(self, method, self.generic_visit)

		return visitor(node)

	def generic_visit(self, node) -> any:
		'generic_visit generally defines the method (pre-order or post-order) and the direction (towards root or toward leaves) of recursion'
		raise ValueError("this {self.__class__.__name__} got {node=}, {type(node)=} and no corresponding visit_* was defined")

	def __repr__(self):
		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods	= [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		name_str = self.__class__.__name__	# in case derived classes dont implement their own __repr__ which they probably wont
		attributes_str = f"{len(attributes)} attributes"
		methods_str = f"{len(methods)} methods"
		return f"<{name_str} at {hex(id(self))}: {attributes_str}, {methods_str}>"

	def __str__(self):
		from collections.abc import Iterable

		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods	= [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		output = f"{self.__class__.__name__} (ID={hex(id(self))})"
		output += f"\nattributes: {len(attributes)} defined"
		for name in attributes:
			value = getattr(self, name)
			if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
				output += f"\n	{name} = {type(value)}, len={len(value)}"
			else:
				output += f"\n	{name} = {value}"
		output += f"\nmethods: {len(methods)} defined"
		for method in methods:
			output += f"\n	{method}()"
		return output

class SimplifyVisitor(NodeVisitor):
	'perform mathematical simplification'

	def visit_add(self, node) -> Node:
		"simplify chained binary 'add' nodes to a single variadic 'sum' node. uses post-order scorched-earth recursion"
		if all(edge.source.metadata != 'add' for edge in iter(node.inputs)):
			return node

		sum_input_nodes: list[Node] = list()

		def visit_node(node: Node) -> None:
			for edge in node.inputs:
				if edge.source.metadata == 'add':
					visit_node(node)	# recursion
				else:
					sum_input_nodes.append(edge.source)

			self.graph.remove_node(edge)	# also removes edges

		sum_node: Node = self.graph.new_node('sum')

		for index, node in enumerate(sum_input_nodes):
			self.graph.new_edge(node, sum_node, index)

		return sum_node

	def visit_mul(self, node) -> Node:
		"simplify chained binary 'mul' nodes to a single variadic 'prod' node. uses post-order scorched-earth recursion"
		if all(edge.source.metadata != 'mul' for edge in iter(node.inputs)):
			return node

		prod_input_nodes: list[Node] = list()

		def visit_node(node: Node) -> None:
			for edge in node.inputs:
				if edge.source.metadata == 'mul':
					visit_node(node)	# recursion
				else:
					prod_input_nodes.append(edge.source)

			dag.remove_node(edge)	# also removes edges

		prod_node: Node = dag.new_node('prod')
		for index, node in enumerate(prod_input_nodes):
			dag.new_edge(node, prod_node, index)

		return prod_node
"""
class AggregateLeavesVisitor(NodeVisitor):
	'aggregate leaves with the same metadata into one node, since this is not done by default by the parser'

	def __init__(self, dag: Dag):
		self.dag: Dag = dag
		raise NotImplementedError("not finished yet")
"""
	
class StringifyVisitor(NodeVisitor):
	'turn a mathematical expression MultiDAG into a string'
	def __init__(
			self, 
			*, 
			pretty: bool = False, 
			spacing: str = ' ',
			cache: dict[Node, str] = None):
		self.pretty: bool = pretty
		self.spacing: str = spacing
		self.cache: dict[Node, str] = dict() if cache is None else cache
	
	def generic_visit(self, node: Node) -> str:
		'any generic function node, like sin(x) that doesnt have any special operator syntax'
		if node in self.cache:
			return self.cache[node]
		
		if node.is_branch:
			args: Iterable[str] = (self.visit(edge.source) for edge in node.inputs) # recursion
			output = f"{node.metadata}({', '.join(args)})"
		elif node.is_leaf:
			output = str(node.metadata)
		else:
			raise RuntimeError(f"did not expect this branch for {node}: {node.is_branch=}, {node.is_leaf=}")
		
		self.cache[node] = output
		return output

	def generic_visit_binary(self, node: Node) -> str:
		'binary operations like +, −, ×, ∕'
		args = [None, None]
		for edge in node.inputs:
			args[edge.metadata] = self.visit(edge.source)	# recursion

		operand: str = node.payload.name

		return f"{args[0]}{self.spacing}{operand}{self.spacing}{args[1]}"

	visit_add = generic_visit_binary
	visit_sub = generic_visit_binary
	visit_mul = generic_visit_binary
	visit_div = generic_visit_binary
	visit_pow = generic_visit_binary
