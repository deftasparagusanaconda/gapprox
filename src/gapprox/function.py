from .mapping import Mapping
from typing import Callable, Iterable
from .relation import Relation

class Function(Relation):
	'a special case of a relation, where each element in the domain always maps to exactly one codomain. it is stored as a dict[any, any]'
	def __init__(
			self,
			domain: set  | Callable[..., bool],
			codomain: set  | Callable[..., bool],
			mapping: dict[any, any] | Callable[..., bool] | Mapping):
		self.domain: set  | Callable[..., bool] = domain
		self.codomain: set  | Callable[..., bool] = codomain
		self.mapping: Mapping = mapping

	def __call__(*args) -> any:
		if not self.domain_has(args):
			raise ValueError("Function does not define {args} in its domain")

		codomain = self.mapping.maps_to(args)

		if not self.codomain_has(codomain):
			raise ValueError("Function does not define {args} in its codomain")

		return codomain

	def domain_has(domain: any) -> bool:
		raise NotImplementedError("not finished yet")

	def codomain_has(codomain: any) -> bool:
		raise NotImplementedError("not finished yet")

	def mapping_has(mapping: any) -> bool:
		raise NotImplementedError("not finished yet")

	def __repr__(self) -> str:
		return f"<Function at {hex(id(self))}: domain={self.domain!r}, codomain={self.codomain!r}, mapping={self.mapping!r}>"

	def __str__(self) -> str:
		output = f"Function at {hex(id(self))}"
		output += f"\n    domain: {type(self.domain)}"
		if isinstance(self.domain, Iterable) and not callable(self.domain):	# because callables can be iterable, strangely
			output += f", len={len(self.domain)}"
		output += f"\n    codomain: {type(self.codomain)}"
		if isinstance(self.codomain, Iterable) and not callable(self.codomain):
			output += f", len={len(self.codomain)}"
		output += f"\n    mapping: {type(self.mapping)}"
		if isinstance(self.mapping, Iterable) and not callable(self.mapping):
			output += f", len={len(self.mapping)}"
		return output


"""
from .operators_dict import operators_dict as default_operators_dict
from .dag import InputNode, FunctionNode, OutputNode, Node, Edge, Dag
from .symbol import Variable, Parameter, Constant
from .misc import ast_op_to_op_dict_key, str_to_ast
from .ast_to_dag_visitor import AstToDagVisitor
from .count import count
from .visitors import EvaluationVisitor
import ast

class Function:
	'represents a mathematical function. it is callable'
	
	def __init__(
			self,
			expression           : OutputNode|ast.AST|str,
			*args,
			dag                  : Dag             = None,
			operators_dict       : dict            = None,
			ast_op_to_op_dict_key: dict            = ast_op_to_op_dict_key
			):		
		self.variables    : list[Variable]      = list()
		self.parameters   : set[Parameter]      = set()
		self.constants    : set[Constant]       = set()
		self.dag = Dag() if dag is None else dag

		if operators_dict is None:
			self.operators_dict: dict[str, callable] = default_operators_dict
		else:
			self.operators_dict: dict[str, callable] = operators_dict

		# populate collections
		for arg in args:
			match arg:
				case Variable():
					self.variables.append(arg)
				case Constant():
					if arg in self.constants:
						raise ValueError(f"{arg} may have been given twice")
					self.constants.add(arg)
				case Parameter():
					if arg in self.parameters:
						raise ValueError(f"{arg} may have been given twice")
					self.parameters.add(arg)
				case _:
					raise TypeError(f"unrecognized argument {arg}: must be Variable, Parameter, or Constant")

		symbols:list[Symbol] = self.variables + list(self.parameters) + list(self.constants)
		
		# check clashing symbol names
		names:list[str] = list(symbol.name for symbol in symbols)
		if len(names) != len(set(names)):
			from collections import Counter
			counts = Counter(names)
			dupes = [(item, count) for item, count in counts.items() if count > 1]
			raise ValueError(f"detected clashing symbol names: {dupes}")		

		match expression:
			case OutputNode():
				self.outputnode = expression
			case ast.AST():
				ast_to_dag_visitor = AstToDagVisitor(
						dag                   = self.dag, 
						variables             = self.variables,
						parameters            = self.parameters,
						constants             = self.constants,
						ast_op_to_op_dict_key = ast_op_to_op_dict_key
				)
				
				root_node = ast_to_dag_visitor.visit(expression)
				outputnode = self.dag.new_outputnode()
				self.dag.new_edge(root_node, outputnode, 0)
				self.outputnode = outputnode
			
			case str():
				ast_tree = str_to_ast(expression)
				ast_to_dag_visitor = AstToDagVisitor(
						dag                   = self.dag, 
						variables             = self.variables,
						parameters            = self.parameters,
						constants             = self.constants,
						ast_op_to_op_dict_key = ast_op_to_op_dict_key
				)

				root_node = ast_to_dag_visitor.visit(ast_tree)
				outputnode = self.dag.new_outputnode()
				self.dag.new_edge(root_node, outputnode, 0)
				self.outputnode = outputnode

			case _:
				raise ValueError(f"unrecognized {expression!r}: must be str, ast.AST, or OutputNode")
			
	def evaluate(self, *args) -> any:
		'perform mathematical evaluation using gapprox.visitors.EvaluationVisitor'
		if len(args) != len(self.variables):
			raise ValueError(f"takes exactly {len(self.variables)} arguments")

		inputnode_payload_subs = dict((self.variables[i], args[i]) for i in range(len(self.variables)))
		evaluation_visitor = EvaluationVisitor(inputnode_payload_subs = inputnode_payload_subs, functionnode_payload_subs = self.operators_dict)

		return evaluation_visitor.visit(self.outputnode)
		
	__call__ = evaluate # makes the Function callable (obv lol)
		
	def to_callable(self) -> callable:
		'convert the heavy Function to a fast python function. this method is nowhere near done or made yet'
		# return compile(self.dag)
		return self

	def __repr__(self):
		variables_str = f"{len(self.variables)} Variable"
		parameters_str = f"{len(self.parameters)} Parameter"
		constants_str = f"{len(self.constants)} Constant"
		return f"<Function at {hex(id(self))}: {variables_str}, {parameters_str}, {constants_str}>"
	
	def __str__(self):
		output = f"Function at {hex(id(self))}"
		output += f"\nvariables    : {type(self.variables)}, count={count(self.variables)}, length={len(self.variables)}"
		for variable in self.variables:
			output += f"\n    {variable!r}"
		output += f"\nparameters   : {type(self.parameters)}, count={count(self.parameters)}, length={len(self.parameters)}"
		for parameter in self.parameters:
			output += f"\n    {parameter!r}"
		output += f"\nconstants    : {type(self.constants)}, count={count(self.constants)}, length={len(self.constants)}"
		for constant in self.constants:
			output += f"\n    {constant!r}"
		output += f"\ndag           : {self.dag!r}"
		output += f"\noutputnode    : {self.outputnode!r}"
		output += f"\noperators_dict: {type(self.operators_dict)}, length={len(self.operators_dict)}"
		return output
"""
