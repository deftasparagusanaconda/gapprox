from .graph import Node, MultiDAG
from collections import Counter
from .ast_to_multidag_visitor import AstToMultiDAGVisitor
from . import misc
from . import visitors
import gapprox
from collections.abc import Iterable
from typing import Any, Callable
from .symbol import Symbol

DEFAULT_ROOT_NODE_PAYLOAD = None

class Expression:
	"""represents a mathematical expression. it is evaluable and callable. the canonical storage is as a MultiDAG, because it reveals the most structure about a math expression

	context given in methods like .evaluate() or .to_str() are only temporary substitutions
	"""
		
	def __init__(self, root: Node, graph: MultiDAG, *, context: dict[Symbol, Any] = None):
		self.root: Node = root
		self.graph: MultiDAG = graph
		self.context: dict[Symbol, Any] = gapprox.default_context.copy() if context is None else context
	
	@classmethod
	def from_str(cls, string: str, *, graph: MultiDAG = None, context: dict[Symbol, Any] = None, ast_to_multidag_visitor: AstToMultiDAGVisitor = None) -> 'Expression':
		
		graph: MultiDAG = MultiDAG() if graph is None else graph	# create its own MultiDAG, if required
		ast_to_multidag_visitor: AstToMultiDAGVisitor = AstToMultiDAGVisitor(graph) if ast_to_multidag_visitor is None else ast_to_multidag_visitor

		ast_tree = misc.str_to_ast(string)
		top_node = ast_to_multidag_visitor.visit(ast_tree)
		root = graph.new_node(DEFAULT_ROOT_NODE_PAYLOAD)
		graph.new_edge(top_node, root)
		
		expression = cls(root, graph, context = context)
		return expression
	
	@property
	def variables() -> set[str]:
		raise NotImplementedError
		# return a set of variables by traversing the graph. implemented as a dynamic property since it is not mathematically intrinsic for an expression to know its variables. also prevents bad method design, especially with .evaluate checking if kwargs satisfies its variables. it should not do that check.
	
	def evaluate(self, substitutions: dict[Any: Any], *, context: dict[Symbol: Any] = None) -> Any:
		'evaluate the expression'
		context: dict[Symbol, Any] = self.context.copy() if context is None else context
		
		substitutions = substitutions.copy()
		
		substitutions.update(context)
		
		def evaluate_node(node: Node) -> any:
			if node.is_leaf:
				return substitutions[node.metadata] if node.metadata in substitutions else node.metadata	# termination
			else:
				function = substitutions[node.metadata] if node.metadata in substitutions else node.metadata
				arguments = [None] * len(node.inputs)
				for edge in node.inputs:
					arguments[edge.metadata] = evaluate_node(edge.source) # recursion
				
				return function(*arguments)	# termination
		
		root_input = next(iter(self.root.inputs)).source
		
		return evaluate_node(root_input)
		
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

		root_input = next(iter(self.root.inputs)).source
		return stringify_visitor.visit(root_input)

	def compile(self, apply_context: bool = True, ) -> Callable[[Any, ...], Any]:
		string = self.to_str()

		def evaulate_expression(**kwargs):
			return eval(string)
			
		return evaluate_expression

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

# this orderedexpression seemed like a good idea but anything that is an expression should straight up just not know the order of its variables. whatever uses the expression for something should store its own order of arguments if it needs it. it shouldnt make the expression store the order. its not intrinsic to the expression.
'''
class OrderedExpression:
	'conceptually just a wrapper for an Expression and an order of variables stored together. it enables an Expression to be evaluated not using a substitution dict but by taking substitutions positionally'
	def __init__(self, expression: str | Expression, *args):
		'can create an Expression from a str for convenience'

		self.order: Sequence[any] = args

		if isinstance(expression, Expression):
			self.expression: Expression = expression
		if not isinstance(expression, str):
			raise ValueError("expression must be str or Expression")

		if self.graph is None:
			self.graph: MultiDAG = MultiDAG()	# creates its own MultiDAG
		if ast_to_multidag_visitor is None:
			ast_to_multidag_visitor = AstToMultiDAGVisitor()
		self.expression: Expression = Expression(expression, ast_to_multidag_visitor = ast_to_multidag_visitor)

	def evaluate(self, *args, **kwargs) -> any:
		'evaluate but with positional arguments'

		if gapprox.debug:
			if not isinstance(self.expression, Expression):
				raise ValueError("expression must be str, Expression")
			if len(args) != len(self.order):
				raise ValueError(f"length mismatch: {len(self.order)=}, {len(args)=}")

		new_context = {key: value for key, value in zip(self.order, args)}
		return self.expression(**new_context)

	__call__ = evaluate
'''
