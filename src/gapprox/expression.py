from .graph import Node, Edge
from collections import Counter
from .ast_to_multidag_visitor import AstToMultiDAGVisitor
from . import misc
from . import visitors
import gapprox
from collections.abc import Sequence 
from typing import Any, Callable
from .context import default_context
from .symbol import Symbol

class Expression:
	"""represents a mathematical expression. it is evaluable and callable. the canonical storage is as a MultiDAG, because it reveals the most structure about a math expression
	
	context given in methods like .evaluate() or .to_str() are only temporary substitutions
	"""
		
	def __init__(self, root: Node, symbols: Sequence[Symbol], *, symbols_dict: dict[str, Symbol] = None) -> None:
		if isinstance(root, str):
			raise TypeError('Expression takes a root node. perhaps you meant Expression.from_str')
		self.root: Node = root
		self._symbols: Sequence[Symbol] = symbols
		self._symbols_dict: dict[str, Symbol] = {symbol.name: symbol for symbol in symbols} if symbols_dict is None else symbols_dict
	
	@classmethod
	def from_str(cls, string: str, symbols: Sequence[Symbol] = None) -> 'Expression':
		symbols = [] if symbols is None else symbols
		symbols_dict: dict[str, Symbol] = {symbol.name: symbol for symbol in symbols}
		
		ast_to_multidag_visitor = AstToMultiDAGVisitor(symbols_dict)
		
		ast_tree = misc.str_to_ast(string)
		top_node = ast_to_multidag_visitor.visit(ast_tree)
		root_node = Node()	# notice the root node doesnt have any payload
		Edge(top_node, root_node)
		
		expression = cls(root_node, symbols, symbols_dict = symbols_dict)
		return expression
	
	def evaluate(self, *args, context: dict[Symbol: Any] = None, **kwargs) -> Any:
		'evaluate the expression'
		context: dict[Symbol, Any] = default_context.copy() if context is None else context.copy()

		# kwargs overrides context
		context.update((self._symbols_dict[key], val) for key, val in kwargs.items())	

		# args overrides context
		for symbol, arg in zip(self._symbols, args):
			context[symbol] = arg
		
		def evaluate_node(node: Node) -> any:
			if node.is_leaf():
				return context.get(node.payload, node.payload)	# termination
			else:
				function = context.get(node.payload, node.payload)
				
				#arguments = sorted(evaluate_node(edge.source) for edge in node.inputs, key = edge.payload)
				arguments = [None] * len(node.inputs)
				for edge in node.inputs:
					arguments[edge.payload] = evaluate_node(edge.source) # recursion
				
				if not callable(function):
					raise Exception(f"No callable bound for symbol {symbol}")

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
	
	#def compile(self, apply_context: bool = True, ) -> Callable[[Any, ...], Any]:
	#	string = self.to_str()
	#
	#	def evaulate_expression(**kwargs):
	#		return eval(string)
	#		
	#	return evaluate_expression

	def __repr__(self):
		return f"<Expression at {hex(id(self))}: root = {self.root!r}, {len(self.context)} contexts>"

	def __str__(self):
		output = f"Expression at {hex(id(self))}"
		output += f"\n    root: {self.root!r}"
		output += f"\n    context: {type(self.context)}, len={len(self.context)}"

		#type_counts = Counter((type(k), type(v)) for k, v in self.context.items())
		#for (ktype, vtype), count in type_counts.items():
		#	output += f"\n        {count} pairs of ({ktype.__name__}: {vtype.__name__})"

		#for key, value in self.context.items():
		#	output += f"\n        {key!r}: {value!r}"
		return output
	
	def __add__(self, value: Any) -> 'Expression':
		return Expression

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
