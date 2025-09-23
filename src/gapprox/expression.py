from .graph import Node, MultiDAG
from collections import Counter
from .ast_to_multidag_visitor import AstToMultiDAGVisitor
from . import misc
from . import visitors
import gapprox
from typing import Iterable

class Expression:
	"""represents a mathematical expression. it is evaluable and callable. the canonical storage is as a MultiDAG, because it reveals the most structure about a math expression

	context given in methods like .evaluate() or .to_str() are only temporary substitutions
	"""
		
	def __init__(
			self, 
			expr: str | Node, 
			context: dict[str, dict[str, any]] = gapprox.default_context, 
			*, 
			graph: MultiDAG = None,
			):
		#'we intentionally do not store a graph, because it muddies up the semantics of an expression. it also causes problems later on in what should own a graph. nothing should own a graph. the user handles their custom graphs.'
		self.context: dict[str, dict[str, any]] = context
		self.graph: MultiDAG = graph

		if self.graph is None:
			self.graph = MultiDAG()	# create its own MultiDAG

		if isinstance(expr, str):
			ast_to_multidag_visitor = AstToMultiDAGVisitor(self.graph)
			ast_tree = misc.str_to_ast(expr)
			top_node = ast_to_multidag_visitor.visit(ast_tree)
			self.root = self.graph.new_node(None)
			edge = self.graph.new_edge(top_node, self.root, 0)
		elif isinstance(expr, Node):
			if not expr.is_root:
				raise ValueError(f"expected {expr} to be a root node")
			self.root = expr
		else:
			raise ValueError("first argument must be str or gapprox.Node")
		
	def evaluate(self, **kwargs):
		"evaluate the expression using keyword arguments as temporary substitutions, like so: expr(x=2) or expr(**{'x': 2})"
		
		context: dict[str, any] = self.context.copy()
		context.update(kwargs)

		 # normalise kwargs → wrap raw values into {'value': ...}
		for key, value in kwargs.items():
			if isinstance(value, dict) and 'value' in value:
				context[key] = value
			else:
				context[key] = {'value': value}
		
		def evaluate_node(node: Node) -> any:
			if node.is_leaf:
				return context[node.metadata]['value'] if node.metadata in context else node.metadata
			else:
				function = context[node.metadata]['callable'] if node.metadata in context else node.metadata
				arguments = [None] * len(node.inputs)
				for edge in node.inputs:
					arguments[edge.metadata] = evaluate_node(edge.source) # recursion
				return function(*arguments)

		return evaluate_node(next(iter(self.root.inputs)).source)

	__call__ = evaluate # makes the expression callable

	def to_str(
			self, 
			*, 
			context: dict[str, dict] = None,
			**kwargs
			) -> str:
		'return the expression as a str'
		new_context = self.context.copy()

		if context is not None:
			new_context.update(context)

		stringify_visitor = visitors.StringifyVisitor(context=new_context, **kwargs)

		return stringify_visitor.visit(next(iter(self.root.inputs)).source)

	def __repr__(self):
		return f"<Expression at {hex(id(self))}: graph=<{self.graph.__class__.__name__} at {hex(id(self.graph))}>, {next(iter(self.root.inputs)).source.metadata!r} → root, {len(self.context)} contexts>"

	def __str__(self):
		output = f"Expression at {hex(id(self))}"
		output += f"\n    graph: {self.graph!r}"
		output += f"\n    root: {self.root!r}"
		output += f"\n    context: {type(self.context)}, len={len(self.context)}"

		#type_counts = Counter((type(k), type(v)) for k, v in self.context.items())
		#for (ktype, vtype), count in type_counts.items():
		#	output += f"\n        {count} pairs of ({ktype.__name__}: {vtype.__name__})"

		#for key, value in self.context.items():
		#	output += f"\n        {key!r}: {value!r}"
		return output
