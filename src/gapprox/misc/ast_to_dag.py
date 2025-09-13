import ast
from ..symbol import Variable, Parameter, Constant
from ..dag import Node, InputNode, FunctionNode, OutputNode, Edge, Dag
from .ast_op_to_op_dict_key import ast_op_to_op_dict_key

# this class is very tied to state. should it be embedded into Function instead?
# i mean.. this function..

class AstToDagAdder(ast.NodeVisitor):
	"""stateful function that adds nodes of an ast to a Dag

	it is a subclass of ast.NodeVisitor, as specified in greentreesnakes.readthedocs.io, but doesnt use generic_visit() to call children, since help(ast.NodeVisitor) says generic_visit() is for when visit_* isnt defined and i trust the help page more and the children may have their type defined so i use visit() instead"""
	def __init__(self, *, dag, variables, parameters, constants, ast_op_to_op_dict_key = ast_op_to_op_dict_key):
		self.dag:Dag = dag
		self.variables:list[Variable] = variables
		self.parameters:list[Parameter] = parameters
		self.constants:list[Constant] = constants
		self.ast_op_to_op_dict_key:dict = ast_op_to_op_dict_key
		
	def visit_Constant(self, node):
		return self.dag.new_node(node.value)
		
	def visit_Name(self, node):
		'btw, this function does not check for duplicate names in variables/constants'
		for variable in self.variables:
			if node.id == variable.name:
				return self.dag.new_node(variable)

		for constant in self.constants:
			if node.id == constant.name:
				return self.dag.new_node(constant)

		raise ValueError(f"{node.id} not in constants={self.constants} nor variables={self.variables}")
	
	def visit_UnaryOp(self, node):
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_node(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported")
		
		operand = self.visit(node.operand)
		self.dag.new_edge(operand, func_node, 0)
		return func_node

	def visit_BinOp(self, node):
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_node(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported (yet!!)")

		left = self.visit(node.left)
		right = self.visit(node.right)
		self.dag.new_edge(left, func_node, 0)
		self.dag.new_edge(right, func_node, 1)
		return func_node
"""
tree = ast.parse('x+3/4', mode='eval').body

dag = Dag()

AstToDagAdder(dag, None, None).visit(tree)
dag.debug_summary()
"""

def ast_to_dag(ast_tree:ast.AST, dag:Dag):
	'convert an ast tree to nodes and add them to a Dag'
	
	# initialize the ast node visitor
	ast_to_dag_adder = AstToDagAdder(
			dag=dag, 
			variables = variables, 
			constants = constants, 
			ast_op_to_op_dict_key = ast_op_to_op_dict_key)
	
	# to connect the last decoded ast node with an outputnode
	latest_node = ast_to_dag_adder.visit(ast_tree)
	expr_
	outputnode = dag.new_outputnode()
	dag.new_edge(latest_node, output_node, 0)
	
	return outputnode

# why does ast_to_dag need to know variables and constants? wouldnt ast already know them from context?
