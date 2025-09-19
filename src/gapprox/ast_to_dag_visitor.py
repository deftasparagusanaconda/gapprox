import ast
from .dag import Node, Edge, Dag
from .misc import ast_op_to_op_dict_key

class AstToDagVisitor(ast.NodeVisitor):
	'stateful function that adds nodes of an ast to a Dag'
	def __init__(self, dag: Dag, ast_op_to_op_dict_key: dict[ast.AST, str] = ast_op_to_op_dict_key):
		self.dag: Dag = dag
		#self.context: dict[str, any] = context
		self.ast_op_to_op_dict_key: dict[ast.AST, str] = ast_op_to_op_dict_key
	
	def generic_visit(self, node: Node) -> None:
		raise NotImplementedError(f"critical error! {node!r} of type {type(node)!r} is not recognized. please report this")
		
	def visit_Constant(self, node: Node) -> Node:	# a number, like 2 in '2+x'
		return self.dag.new_node(node.value)
	
	def visit_Name(self, node: Node) -> Node:
		return self.dag.new_node(node.id)

	def visit_UnaryOp(self, node: Node) -> Node:
		op = type(node.op)

		if op in self.ast_op_to_op_dict_key:
			raise NotImplementedError(f"{node.op} not supported")

		func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		operand = self.visit(node.operand)	# recursion
		self.dag.new_edge(operand, func_node, 0)
		return func_node

	def visit_BinOp(self, node: Node) -> Node:
		op = type(node.op)

		if op not in self.ast_op_to_op_dict_key:
			raise NotImplementedError(f"{node.op} not supported")

		func_node = self.dag.new_node(ast_op_to_op_dict_key[op])
		left = self.visit(node.left)	# recursion
		right = self.visit(node.right)	# recursion
		self.dag.new_edge(left, func_node, 0)
		self.dag.new_edge(right, func_node, 1)
		return func_node

	def visit_Call(self, node) -> Node:
		op:str = node.func.id
		args:list[Node] = [self.visit(arg) for arg in node.args]	# recursion
		
		# connect args as inputs to op
		func_node = self.dag.new_node(op)
		for index, arg in enumerate(args):
			self.dag.new_edge(arg, func_node, index)
		
		return func_node

	"""
	def visit_Compare(self, node) -> FunctionNode:
		'assumes comparison operators are binary operators'
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
		
	def visit_BoolOp(self, node) -> FunctionNode:
		'uses AND/OR if binary, ALL/ANY if variadic'
		op = type(node.op)

		if op not in self.ast_op_to_op_dict_key:
			raise NotImplementedError(f"{node.op} not supported")

		if len(node.values) == 2:	# binary
			func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
			in1 = self.visit(node.values[0])	# recursion
			in2 = self.visit(node.values[1])	# recursion
			self.dag.new_edge(in1, func_node, 0)
			self.dag.new_edge(in2, func_node, 1)
			return func_node

		if isinstance(node.op, ast.And):
			name = 'all'
		elif isinstance(node.op, ast.Or):
			name = 'any'
		else:
			raise ValueError(f"critical error! {node.op} not recognized")

		tuple_node = self.dag.new_functionnode('tuple')
		func_node = self.dag.new_functionnode(name)
		
		for index, value in enumerate(node.values):
			input = self.visit(value)	# recursion
			self.dag.new_edge(input, tuple_node, index)

		self.dag.new_edge(tuple_node, func_node, 0)
		
		return func_node

	def visit_IfExp(self, node) -> FunctionNode:
		"if else expression. ast formats it like: 'node.body if node.test else node.orelse' and gapprox follows a 'a if b else c' order, instead of a 'if a then b else c' order"
		op = type(node)
		
		if op not in self.ast_op_to_op_dict_key:
			raise NotImplementedError(f"{node.op} not supported")

		func_node = self.dag.new_functionnode(ast_op_to_op_dict_key[op])
		
		body_node:Node = self.visit(node.body)	# recursion
		test_node:Node = self.visit(node.test)	# recursion
		orelse_node:Node = self.visit(node.orelse)	#recursion
		
		self.dag.new_edge(body_node, func_node, 0)
		self.dag.new_edge(test_node, func_node, 1)
		self.dag.new_edge(orelse_node, func_node, 2)

		return func_node

	def visit_Lambda(self, node):
		raise NotImplementedError("the developer is still debating how to represent a lambda function in a DAG. should she represent it as an object? a FunctionNode? an InputNode? its own self-contained Dag? or self-contained Function? these are perplexing questions...")

	def visit_Subscript(self, node):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

	def visit_Attribute(self, node):
		raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

	"""
