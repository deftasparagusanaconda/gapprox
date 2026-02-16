# we kinda *want* something that can update the inputs list for the operators because inputs lists are being dynamically grown which can get pretty expensive, i think. dynamic allocation is always slower than static allocation

import gapprox
from ..graph import NodeVisitor

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
