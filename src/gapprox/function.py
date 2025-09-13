from .operator_dicts import default as operator_dict_default
from .dag import Node, InputNode, FunctionNode, OutputNode, Edge, Dag
from .symbol import Variable, Parameter, Constant
from .misc.ast_op_to_op_dict_key import ast_op_to_op_dict_key
from .misc.ast_to_dag import ast_to_dag
from .misc.str_to_ast import str_to_ast
from .misc.count import count
import ast

class Function:
	"""represents a mathematical function. it can take m inputs for m variables and give n outputs for n expressions"""
	
	def __init__(
			self,
			expression:str|OutputNode|ast.AST,
			*args,
			operator_dict:dict = None,
			ast_op_to_op_dict_key:dict = ast_op_to_op_dict_key
			):
		self.variables:list[Variable] = list()
		self.parameters:list[Parameter] = list()
		self.constants:set[Constant] = set()
		self.dag:Dag = None
		self.outputnode:Node = None
		self.operator_dict:dict = operator_dicts.default.copy() if operator_dict is None else operator_dict
		
		# populate collections
		for arg in args:
			if isinstance(arg, Variable):
				self.variables.append(arg)
			elif isinstance(arg, Constant):
				self.constants.add(arg)
			elif isinstance(arg, Parameter):
				self.variables.add(arg)
			elif isinstance(arg, Dag):
				self.dag = arg
			else:
				raise TypeError(f"unrecognized argument {arg}: must be Variable, Parameter, Constant or Dag")
		"""
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
		"""

		# create dag if not given
		if self.dag is None:
			# need to offload this to a separate function
			self.dag = Dag()
			add_ast_to_dag = AddAstToDag(self.dag, self.variables, self.constants, ast_op_to_op_dict_key=ast_op_to_op_dict_key)

			tree = ast.parse(expression, mode='eval').body
			latest_node = add_ast_to_dag.visit(tree)
			expr_node = self.dag.new_node(expr)
			self.dag.new_edge(latest_node, expr_node, 0)
			self.output_nodes.append(expr_node)
			
	def evaluate(self):
		"""performs a recursive cached/memoized DFS evaluation with a substitution dict. even if there are repeated nodes, this allows it to avoid those. for example, computing x+2 only once in (x+2)*(x+2). this substitution dict is also shared between expressions. so (x+2)/3 and (x+2)/4 would have to compute (x+2) only once and then reuse it.

		if you need to use the substitutions dict it used during evaluation, you can initialize your own dict instance outside the function and then pass it to the arguments. any substitutions it made will be reflected in that instance you passed because dicts are passed by reference :) have fun with that!"""
		return outputnode.substitute(substitutions)
		
	__call__ = evaluate # makes the Function callable lol
		
	def to_callable(self):
		'convert the heavy Function to a fast python function'
		# return compile(self.dag)
		raise NotImplementedError("this is pretty hard to do sry come back later")
	
	def __str__(self):
		output = f"Function (ID={hex(id(self))})"
		output += f"\nvariables    : {type(self.variables)}, count={count(self.variables)}, length={len(self.variables)}"
		for variable in self.variables:
			output += f"\n    {variable!r}"
		output += f"\nparameters   : {type(self.parameters)}, count={count(self.parameters)}, length={len(self.parameters)}"
		for parameter in self.parameters:
			output += f"\n    {parameter!r}"
		output += f"\nconstants    : {type(self.constants)}, count={count(self.constants)}, length={len(self.constants)}"
		for constant in self.constants:
			output += f"\n    {constant!r}"
		output += f"\ndag          : {self.dag!r}"
		output += f"\noutputnode   : {self.output_nodes!r}"
		output += f"\noperator_dict: {type(self.operator_dict)}, count={count(self.operator_dict)}, length={len(self.operator_dict)}"
		return output
