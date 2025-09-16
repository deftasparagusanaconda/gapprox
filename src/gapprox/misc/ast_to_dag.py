import ast
from ..symbol import Symbol, Variable, Parameter, Constant
from ..dag import Node, InputNode, FunctionNode, OutputNode, Edge, Dag
from .ast_op_to_op_dict_key import ast_op_to_op_dict_key

class AstToDagVisitor(ast.NodeVisitor):
	'stateful function that adds nodes of an ast to a Dag'
	def __init__(
			self, 
			*, 
			dag                  :Dag,
			symbols              :dict,
			name_to_symbol_dict  :dict = None,
			ast_op_to_op_dict_key:dict[ast.AST, 'str'] = ast_op_to_op_dict_key
			):
		self.dag:Dag = dag
		self.symbols:list[Symbol] = symbols
		if name_to_symbol_dict is None:
			self.name_symbol_dict:dict[str, Symbol] = dict((symbol.name, symbol) for symbol in symbols)
		self.ast_op_to_op_dict_key:dict = ast_op_to_op_dict_key
		
	def visit_Constant(self, node) -> InputNode:	# a number, like 2 in '2+x'
		return self.dag.new_inputnode(Parameter(node.value))
		
	# this logic is probably wrong. it should return a node, not a Symbol
	def visit_Name(self, node) -> Node:
		if node.id in self.name_symbol_dict:
			symbol = self.name_symbol_dict[node.id]
		else:
			raise ValueError(f"{node.id} not found in symbols")

		for inputnode in self.dag.inputnodes:
			if isinstance(inputnode.payload, Symbol) and inputnode.payload.name == symbol:
				return inputnode
		
		return self.dag.new_inputnode(symbol)

	def visit_UnaryOp(self, node) -> Node:
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported")
		
		operand = self.visit(node.operand)
		self.dag.new_edge(operand, func_node, 0)
		return func_node

	def visit_BinOp(self, node) -> Node:
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported")

		left = self.visit(node.left)
		right = self.visit(node.right)
		self.dag.new_edge(left, func_node, 0)
		self.dag.new_edge(right, func_node, 1)
		return func_node

#	def visit_Call(self, node):
#	def visit_Attribute(self, node):
#	def visit_Subscript(self, node):
#	def visit_Compare(self, node):
#	def visit_BoolOp(self, node):
#	def visit_IfExp(self, node):
#	def visit_Lambda(self, node):
"""
tree = ast.parse('x+3/4', mode='eval').body

dag = Dag()

AstToDagAdder(dag, None, None).visit(tree)
dag.debug_summary()
"""

# why does ast_to_dag need to know variables and constants? wouldnt ast already know them from context?
# i dont know
