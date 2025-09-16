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

	def generic_visit(self, node):
		raise NotImplementedError(f"{node} is currently not supported. please report this")
		
	# this logic is probably wrong. it should return a node, not a Symbol
	def visit_Name(self, node) -> InputNode:
		if node.id in self.name_symbol_dict:
			symbol = self.name_symbol_dict[node.id]
		else:
			raise ValueError(f"{node.id} not found in symbols")

		for inputnode in self.dag.inputnodes:
			if isinstance(inputnode.payload, Symbol) and inputnode.payload.name == symbol:
				return inputnode
		
		return self.dag.new_inputnode(symbol)

	def visit_UnaryOp(self, node) -> FunctionNode:
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported")
		
		operand = self.visit(node.operand)	# recursion
		self.dag.new_edge(operand, func_node, 0)
		return func_node

	def visit_BinOp(self, node) -> FunctionNode:
		op = type(node.op)
		if op in self.ast_op_to_op_dict_key:
			func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		else:
			raise NotImplementedError(f"{node.op} not supported")

		left = self.visit(node.left)	# recursion
		right = self.visit(node.right)	# recursion
		self.dag.new_edge(left, func_node, 0)
		self.dag.new_edge(right, func_node, 1)
		return func_node

	def visit_Call(self, node) -> FunctionNode:
		op:str = node.func.id
		args:list[Node] = [self.visit(arg) for arg in node.args]	# recursion
		
		# connect args as inputs to op
		func_node = self.dag.new_functionnode(op)
		for index, arg in enumerate(args):
			self.dag.new_edge(arg, func_node, index)

		return func_node

	def visit_Compare(self, node) -> FunctionNode:
		"assumes comparison operators are binary operators"
		args: list[Node] = [self.visit(arg) for arg in [node.left] + node.comparators]	# recursion

		func_nodes: list[Node] = []
		for index, op in enumerate(node.ops):
			op_type = type(op)
			if op_type not in self.ast_op_to_op_dict_key:
				raise NotImplementedError(f"{op} not supported")
			func_node = self.dag.new_functionnode(self.ast_op_to_op_dict_key[op_type])
			self.dag.new_edge(args[index], func_node, 0)
			self.dag.new_edge(args[index+1], func_node, 1)
			func_nodes.append(func_node)

		if len(func_nodes) == 1:  # simple unchained case
			return func_nodes[0]

		# route all to a tuple wrapper
		tuple_funcnode = self.dag.new_functionnode('tuple')
		for index, func_node in enumerate(func_nodes):
			self.dag.new_edge(func_node, tuple_funcnode, index)
		
		# route tuple wrapper to all()
		all_funcnode = self.dag.new_functionnode('all')
		self.dag.new_edge(tuple_funcnode, all_funcnode, 0)

		return all_funcnode

#	def visit_BoolOp(self, node):
#	def visit_IfExp(self, node):
#	def visit_Lambda(self, node):
#	def visit_Subscript(self, node):
#	def visit_Attribute(self, node):

# why does ast_to_dag need to know variables and constants? wouldnt ast already know them from context?
# i dont know
