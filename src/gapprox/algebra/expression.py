from ..graph import Node, Edge
from collections import Counter
from .ast_visitor import AstVisitor
from . import visitors
import gapprox
from collections.abc import Iterable
from typing import Any, Callable
from .dicts import default_evaluate_dict, default_parse_dict, default_translate_dict
import ast
from .symbol import Symbol

class Expression(Node):
	'represents a mathematical expression. it is evaluable and callable. the canonical storage is as a MultiDAG, because it reveals the most structure about a math expression'
		
	@classmethod
	def from_str(
			cls,
			string: str,
			symbols: Iterable[Symbol] = set(),
			parse_dict: dict[str, Symbol] = default_parse_dict,
			translate_dict: dict[ast.AST, Symbol] = default_translate_dict,
			) -> 'Expression':
		symbols_dict: dict[str, Symbol] = {symbol.name: symbol for symbol in symbols}
		
		ast_visitor:AstVisitor = AstVisitor(symbols_dict = symbols_dict, parse_dict = parse_dict, translate_dict = translate_dict)
		
		ast_tree: ast.AST = parse(expr, mode='eval').body
		return ast_visitor.visit(ast_tree)
	
	def evaluate(self, substitutions: Mapping[Symbol: Any] = None, default_substitutions: Mapping[Symbol: Any] = None) -> Any:
		'evaluate the expression'
		# we could rely on kwargs as the dict. but we dont. do you know why?
		# because kwargs: dict[str, Any] requires us to decode the str to a Symbol. this is bad. this means the str is the marker. this is wrong
		# instead we pass substitutions: dict[Symbol, Any], implying that Symbol is the marker.
		
		substitutions: Mapping[Symbol, Any] = dict() if substitutions is None else substitutions
		default_substitutions: Mapping[Symbol, Any] = default_evaluate_dict if default_substitutions is None else default_substitutions
		
		# substitutions overrides default_substitutions
		subs: Mapping[Symbol: Any] = default_substitutions | substitutions
		
		def evaluate_node(node: Node) -> any:
			if node.is_leaf():
				return subs.get(node.payload, node.payload)	# termination
			else:
				function = subs.get(node.payload, node.payload)
				
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
		return f"<Expression at {hex(id(self))}: payload = {self.payload!r}>"

	#def __add__(self, value: Any) -> 'Expression':
	#	return Expression

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

