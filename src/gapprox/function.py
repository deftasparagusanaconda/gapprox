from .operator_dicts import default as operator_dict_default
from .dag import Dag
from .node import Node
from .variable import Variable
from .constant import Constant
from .expression import Expression
from .add_ast_to_dag import AddAstToDag
from .misc.ast_op_to_op_dict_key import ast_op_to_op_dict_key

class Function:
	"""represents a mathematical function. it can take m inputs for m variables and give n outputs for n expressions"""

	def __init__(
			self, 
			*args, 
			operator_dict:dict = operator_dict_default, 
			ast_op_to_op_dict_key:dict = ast_op_to_op_dict_key
			):
		self.operator_dict:dict = operator_dict
		self.variables:list[Variable] = list()
		self.constants:set[Constant] = set()
		self.dag:Dag = None
		self.output_nodes:list[Node] = list()

		expressions:list[Expressioon] = list()

		# populate collections
		for arg in args:
			if isinstance(arg, Constant):
				self.constants.add(arg)
			elif isinstance(arg, Variable):
				self.variables.append(arg)
			elif isinstance(arg, Expression):
				self.expressions.append(arg)
			elif isinstance(arg, Dag):
				if self.dag is not None:
					raise ValueError("only one Dag allowed for Function constructor")
				self.dag = arg
			elif isinstance(arg, str):
				raise TypeError(f"cannot take string as direct argument. try passing gapprox.Expression({arg}) instead")
			else:
				raise TypeError(f"unrecognized argument {type(arg)}. must be Constant, Variable, Expression, or Dag. ")

		# check clashing variable/constant names
		names = list(var.name for var in self.variables) + list(const.name for const in self.constants)
		if len(names) != len(set(names)):
			from collections import Counter
			var_names = list(var.name for var in self.variables)
			const_names = list(const.name for const in self.constants)

			counts = Counter(var_names)
			duplicates = [item for item, count in counts.items() if count > 1]
			if len(duplicates) != 0:
				raise ValueError(f"duplicate variable names: {duplicates}")

			counts = Counter(const_names)
			duplicates = [item for item, count in counts.items() if count > 1]
			if len(duplicates) != 0:
				raise ValueError(f"duplicate constant names: {duplicates}")

			duplicates = set(var_names) & set(const_names)
			if len(duplicates) != 0:
				raise ValueError(f"clashing variable and constant names: {duplicates}")

			raise ValueError(f"found clashing variable/constant names but could not identify which")

		# create dag if not given
		if self.dag is None:
			import ast

			self.dag = Dag()
			add_ast_to_dag = AddAstToDag(self.dag, self.variables, self.constants, ast_op_to_op_dict_key=ast_op_to_op_dict_key)

			for expr in self.expressions:
				tree = ast.parse(expr.value, mode='eval').body
				latest_node = add_ast_to_dag.visit(tree)
				expr_node = self.dag.new_node(expr)
				self.dag.new_edge(latest_node, expr_node, 0)
				self.output_nodes.append(expr_node)
			
	def evaluate(self, substitutions:dict=dict()):
		"""performs a recursive cached/memoized DFS evaluation with a substitution dict. even if there are repeated nodes, this allows it to avoid those. for example, computing x+2 only once in (x+2)*(x+2). this substitution dict is also shared between expressions. so (x+2)/3 and (x+2)/4 would have to compute (x+2) only once and then reuse it.

		if you need to use the substitutions dict it used during evaluation, you can initialize your own dict instance outside the function and then pass it to the arguments. any substitutions it made will be reflected in that instance you passed because dicts are passed by reference :) have fun with that!"""
		return list(node.inputs[0].source.substitute(substitutions) for node in self.output_nodes)
	
	__call__ = evaluate
		
	def to_callable(self):
		'convert the heavy Function to a fast python function'
		# return compile(self.dag)
		raise NotImplementedError("this is pretty hard to do sry come back later")
	
	def topological_sort(self):
		raise NotImplementedError("will use python's graphlib. soon!")
	
	def __repr__(self):
		return f"<gapprox.Function(dag={self.dag!r})>"

	__str__ = __repr__

	def pretty_print(self):
		from os import get_terminal_size

		rows, cols = get_terminal_size()

		print(' gapprox.Function().pretty_print() '.center(rows, '-'))
		print()
		print('operator_dict:', self.operator_dict)
		print('expressions  :', self.expressions)
		print('variables    :', self.variables)
		print('constants    :', self.constants)
		print('dag          :', self.dag)
		print('output_nodes :', self.output_nodes)
		print()
		print(' hope everything is okay... '.center(rows, '-'))
