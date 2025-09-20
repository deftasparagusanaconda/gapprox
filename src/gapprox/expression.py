from .dag import Node, Dag
from collections import Counter
from .ast_to_dag_visitor import AstToDagVisitor
from . import misc
from . import visitors
import gapprox
from typing import Iterable

class Expression:
	"""represents a mathematical expression. it is evaluable and callable. the canonical storage is as a DAG, because it reveals the most structure about a math expression

	context given in methods like .evaluate() or .to_str() are only temporary substitutions
	"""
		
	def __init__(
			self, 
			expr: str | Node, 
			context: dict[str, any] = gapprox.default_context, 
			*, 
			dag = None,
			):
		self.context = context
		self.dag = dag

		if dag is None:
			self.dag = Dag()	# create its own Dag

		if isinstance(expr, str):
			ast_to_dag_visitor = AstToDagVisitor(self.dag)
			ast_tree = misc.str_to_ast(expr)
			top_node = ast_to_dag_visitor.visit(ast_tree)
			self.root = self.dag.new_node(None)
			edge = self.dag.new_edge(top_node, self.root, 0)
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
			if len(node.inputs) == 0:
				return context[node.payload]['value'] if isinstance(node.payload, str) else node.payload
			else:
				function = context[node.payload]['callable'] if isinstance(node.payload, str) else node.payload
				arguments = tuple(evaluate_node(edge.source) for edge in node.inputs)
				return function(*arguments)

		return evaluate_node(self.root.inputs[0].source)

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

		return stringify_visitor.visit(self.root.inputs[0].source)

	def __repr__(self):
		return f"<Expression at {hex(id(self))}: dag=<Dag at {hex(id(self.dag))}>, {self.root.inputs[0].source.payload!r} → root, {len(self.context)} contexts>"

	def __str__(self):
		output = f"Expression at {hex(id(self))}"
		output += f"\n    dag: {self.dag!r}"
		output += f"\n    root: {self.root!r}"
		output += f"\n    context: {type(self.context)}, len={len(self.context)}"

		#type_counts = Counter((type(k), type(v)) for k, v in self.context.items())
		#for (ktype, vtype), count in type_counts.items():
		#	output += f"\n        {count} pairs of ({ktype.__name__}: {vtype.__name__})"

		#for key, value in self.context.items():
		#	output += f"\n        {key!r}: {value!r}"
		return output
