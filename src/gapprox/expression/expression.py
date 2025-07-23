# from graphlib import TopologicalSorter

class Node:
	'a node of a directed acyclic graph (DAG). it can store local edges for quick local traversal. payload is immutable but inputs and outputs are mutable. it is managed by gapprox.Dag'
	
	def __init__(self, payload:any):
		self.inputs:list['Edge'] = list()
		self.payload = payload
		self.outputs:set['Edge'] = set()

	def evaluate(self, substitutions:dict={}):
		'perform a cached recursive DFS evaluation with given substitutions'
		if self in substitutions:
			return substitutions[self]
		if callable(self.payload):
			result = self.payload(*(input.source.evaluate(substitutions) for input in self.inputs))
		else:
			result = substitutions.get(self.payload, self.payload)
		substitutions[self] = result
		return result
	"""
	@staticmethod
	def connect(source:Node, target:Node, index:int):
		while len(target.inputs) <= index:
			target.inputs.append(None)
		if target.inputs[index]:
			raise ValueError(f"target.inputs[{index}] is already {target.inputs[index]}")
		target.inputs[index] = source
		source.outputs.add(target)

	@staticmethod
	def disconnect(source:Node, target:Node, index:int):
		if len(target.inputs)<=index or target.inputs[index]!=source:
			raise ValueError(f"target.inputs[{index}] does not have Node {source}")
		if target not in source.outputs:
			raise ValueError(f"source.outputs does not have {target}")
		target.inputs[index] = None
		source.outputs.remove(target)
	"""
	def is_input(self):
		return len(self.inputs) == 0

	def is_branch(self):
		return len(self.inputs)!=0 and len(self.outputs)!=0

	def is_output(self):
		return len(self.outputs) == 0

	def __repr__(self):
		return f"<Node(payload={self.payload!r}, inputs={self.inputs!r}, outputs={self.outputs!r})>"

	def __str__(self):
		return str(self.payload)

	def __hash__(self):
		return id(self)

	def __eq__(self, other):
		return other is self

class Edge:
	'an edge of a directed acyclic graph. it stores source, target, and since inputs of a Node are positional, it also stores the position as index. these are immutable but other metadata such as weight are mutable. it is managed by gapprox.Dag'
	def __init__(self, source:Node, target:Node, index:int):
		self.source = source
		self.target = target
		self.index = index

	def __repr__(self):
		return f"<Edge(source={self.source}, target={self.target}, index={self.index})>"

	def __str__(self):
		return f"{self.source} to {self.target} at {self.index}"

	def __hash__(self):
		return id(self)

	def __eq__(self, other):
		return other is self

class Dag:
	'handles all DAG-related operations. it handles Nodes and Edges. you may either create new ones with new_node and new_edge or add with add_node and add_edge. you may remove with remove_node and remove_edge'

	def __init__(self, nodes:set[Node]=None, edges:set[Edge]=None):
		self.nodes = nodes or set()
		self.edges = edges or set()

	def new_node(self, payload:any):
		'create a new node instance and add it. also return it'
		node = Node(payload)
		self.add_node(node)
		return node

	def try_new_node(self, payload:any):
		'create a new node instance and add it. also return it'
		node = Node(payload)
		self.try_add_node(node)
		return node

	def new_edge(self, source:Node, target:Node, index:int):
		'create a new edge instance and add it. also return it'
		edge = Edge(source, target, index)
		self.add_edge(edge)
		return edge

	def try_new_edge(self, source:Node, target:Node, index:int):
		'create a new edge instance and add it. also return it'
		edge = Edge(source, target, index)
		self.try_add_edge(edge)
		return edge
	
	def add_node(self, node:Node):
		'add a node. raises an error if the node already exists'
		if node in self.nodes:
			raise ValueError(f"{node} already exists")
		self.nodes.add(node)

	def try_add_node(self, node:Node):
		'add a node. does not raise an error if the node already exists'
		self.nodes.add(node)

	def remove_node(self, node:Node):
		'remove a node, and all corresponding edges. raises an error if the node or its corresponding edges are not found'
		if node not in self.nodes:
			raise ValueError(f"{node} does not exist")
		self.nodes.remove(node)
		for edge in node.inputs+node.outputs:
			if edge not in self.edges:
				raise ValueError(f"{edge} does not exist")
			self.remove_edge(edge)
	
	def try_remove_node(self, node:Node):
		'remove a node, and all corresponding edges. does not raise an error if the node or its corresponding edges are not found'
		self.nodes.discard(node)
		for edge in node.inputs+node.outputs:
			self.discard_edge(edge)

	def add_edge(self, edge:Edge):
		'add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge'
		if edge in self.edges:
			raise ValueError(f"{edge} already exists")
		elif edge in edge.source.outputs:
			raise ValueError(f"{edge} already exists in its source's outputs")
		if len(edge.target.inputs)>edge.index:
			if edge.target.inputs[edge.index]!=None:
				raise ValueError(f"{edge.target.inputs[edge.index]} already exists in its target's input")
		self.edges.add(edge)
		edge.source.outputs.add(edge)
		while len(edge.target.inputs) <= edge.index:
			edge.target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

	def try_add_edge(self, edge:Edge):
		'add an edge and update its source and target to know that edge. does not raise an error if the edge already exists, or its source or target already know that edge'
		self.edges.add(edge)
		edge.source.outputs.add(edge)
		while len(edge.target.inputs) <= edge.index:
			target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

	def remove_edge(self, edge:Edge):
		'remove an edge and update its source and target to forget that edge. raises an error if the edge is not found, or its source or target do not know that edge'
		if edge not in self.edges:
			raise ValueError(f"{edge} does not exist")
		elif edge not in edge.source.outputs:
			raise ValueError(f"{edge} does not exist in its target's outputs")
		elif edge.target.inputs[edge.index] != edge:
			raise ValueError(f"{edge.target.inputs[edge.index]} is not {edge}")
		self.edges.remove(edge)
		edge.source.outputs.remove(edge)
		edge.target.inputs[edge.index] = None

	def try_remove_edge(self, edge:Edge):
		'remove an edge, and update its source and target to forget that edge. does not raise an error if the edge is not found, or its source or target do not know that edge'
		self.edges.discard(edge)
		edge.source.outputs.discard(edge)
		edge.target.inputs[edge.index] = None

class Expression:
	'store a mathematical expression. also handles mathematical operations on an expression'

	def __init__(self, input:str|Dag=None):
		if isinstance(input, str):
			from ast import parse
			self.dag = Expression.ast_to_node(parse(expr, mode='eval').body)
			# USES AI-GENERATED CODE. ONLY MEANT FOR EARLY TESTING
		self.dag = input

	"""
	def __add__(self):
	def __radd__(self):
	def __mul__(self):
	def __pow__(self):
	def __neg__(self):
	"""

	def evaluate(self, substitutions:dict=None):
		return self.root.evaluate(substitutions)
		
	def to_callable(self):
		'convert the heavy Expression to a fast python function'
		
	__call__ = evaluate

	def topological_sort(self):
		return "haha i didnt implement this yet!!"

	def __repr__(self):
		return f"<Expression(dag={self.dag!r})>"

	__str__ = __repr__

	@staticmethod
	def ast_to_node(node):
		'THIS METHOD IS AI-GENERATED AND IS ONLY FOR EARLY TESTING'
		import ast

		if isinstance(node, ast.BinOp):
			left = Expression.ast_to_node(node.left)
			right = Expression.ast_to_node(node.right)

			if isinstance(node.op, ast.Add):
				payload = lambda a, b: a + b
			elif isinstance(node.op, ast.Sub):
				payload = lambda a, b: a - b
			elif isinstance(node.op, ast.Mult):
				payload = lambda a, b: a * b
			elif isinstance(node.op, ast.Div):
				payload = lambda a, b: a / b
			elif isinstance(node.op, ast.Pow):
				payload = lambda a, b: a ** b
			else:
				raise NotImplementedError(f"Operator {node.op} not supported")

			node_obj = Node(payload)
			node_obj.inputs.extend([left, right])
			left.outputs.add(node_obj)
			right.outputs.add(node_obj)
			return node_obj

		elif isinstance(node, ast.UnaryOp):
			operand = Expression.ast_to_node(node.operand)

			if isinstance(node.op, ast.USub):
				payload = lambda a: -a
			elif isinstance(node.op, ast.UAdd):
				payload = lambda a: +a
			else:
				raise NotImplementedError(f"Unary operator {node.op} not supported")

			node_obj = Node(payload)
			node_obj.inputs.append(operand)
			operand.outputs.add(node_obj)
			return node_obj

		elif isinstance(node, ast.Constant):
			return Node(node.value)

		elif isinstance(node, ast.Name):
			return Node(node.id)  # variable leaf node

		else:
			raise NotImplementedError(f"AST node type {type(node)} not supported")

"""

class Dag:
	"holds a set of nodes, which represent one graph"

	def __init__(self, nodes=set()):
		self.nodes = nodes

	def add_node(self, node):
		self.nodes.add(node)

	def remove_node(self, node):
		self.nodes.remove(node)

	@staticmethod
	def connect(input, output, index=None):
		input.add_output(output)
		output.add_input(input, index)

	@staticmethod
	def disconnect(input, output, index=None):
		input.remove_output(output)
		output.remove_input(index)

	#def check_cyclicity(something):
	#def get_edge_list(self):
		# return a list of all edges enclosed by the DAG
		# edges that point to nodes outside the list are ignored
"""
"""
def toggle_edge(source:Node, target:Node, index:int):
	while len(target.inputs) <= index:
		target.inputs.append(None)

	if target.inputs[index] is source:  # currently connected, so disconnect
		target.inputs[index] = None
		source.outputs.remove(target)

	elif target.inputs[index] is None:  # currently disconnected, so connect
		target.inputs[index] = source
		source.outputs.add(target)

    else:
		raise Exception(f"target.inputs[{index}] is already connected to {target.inputs[index]}, cannot toggle edge with {source}")
"""

"""
from abc import ABC, abstractmethod

class _Node(ABC):
	"arbitrary base class for NodeInput, NodeFunction, NodeOutput"

	@abstractmethod
	def evaluate(self, substitutions:dict=None):
		...

class _NodeInput(Node):
	"holds a parameter (variable/constant/nullary function...) of a DAG. NodeInput has no inputs, but multiple outputs"

	def __init__(self, value:any):
		self.outputs = set()
		self.value = value

	def add_output(self, output):
		self.outputs.add(output)

	def remove_output(self, output):
		self.outputs.remove(output)

	def evaluate(self, substitutions:dict=None):
		if callable(self.value):
			return self.value()
		elif self.value in substitutions:
			return substitutions[self.value]
		return self.value

class _NodeFunction(Node):
	"a function/operator node of a DAG. NodeFunction has inputs and outputs"

	def __init__(self, function:callable):

		if not callable(function):
			raise TypeError(f"{function} is not callable")

		self.function = function

		from inspect import signature, Parameter
		params = signature(function).parameters.values()

		# check if it has *args
		for param in params:
			if param.kind == Parameter.VAR_POSITIONAL:
				self.variadic = True
			elif param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
				self.arity
			else:
				self.variadic = False

		if self.arity == 0 and self.variadic is False:
			raise ValueError(f"zero input functions not allowed. implement {function} as NodeInput instead")

		# count required positional args
		self.arity = len(p for p in params if p.kind is Parameter.POSITIONAL_ONLY)

		self.inputs = [None]*self.arity
		self.outputs = set()

	def add_input(self, input, index):
		self.inputs[index] = input

	def add_output(self, output):
		self.outputs.add(output)

	def remove_input(self, index):
		self.inputs[index] = None

	def remove_output(self, output):
		self.outputs.remove(output)

	def evaluate(self, substitutions:dict=None):
		if self.inputs:
			return self.function(tuple(input.evaluate(substitutions) for input in self.inputs))
		else:
			raise ValueError("FunctionNode has no inputs")

# a        POSITIONAL_ONLY
# b=1      POSITIONAL_ONLY
# /        (positional marker)
# d=2      POSITIONAL_OR_KEYWORD
# *args    VAR_POSITIONAL
# e        KEYWORD_ONLY
# f=3      KEYWORD_ONLY
# **kwargs VAR_KEYWORD

class _NodeOutput(Node):
	"the root node of an expression. the grandpa of all nodes in an expression. NodeOutput has 1 input, no outputs"

	def __init__(self, input=None):
		self.input = None

	def add_input(self, input):
		if self.input is None:
			self.input = input
		else:
			raise ValueError(f"OutputNode {self.__name__} already holds {self.input}")
		#should this allow setting if self.input is already set?

	def remove_input(self):
		if self.input is None:
			raise ValueError(f"OutputNode {self.__name__} has no input set")
		else:
			self.input = None
		# should this allow unsetting if self.input is already None?

	def evaluate(self, substitutions:dict=None):
		if self.input is None:
			raise ValueError(f"OutputNode {self.__name__} has no input set")
		else:
			return self.input.evaluate(substitutions)

# need to find a way to represent variables in the system
"""
"""
import operator

a = Node(2)
b = Node(3)
c = Node('x')
plus = Node(operator.add)
Node.connect(a, plus, 0)
Node.connect(b, plus, 1)
print(plus.evaluate())          # 5
print(plus.evaluate({2: 3}))    # 6
Node.disconnect(b, plus, 1)
Node.connect(c, plus, 1)
print(plus.evaluate({'x': 10})) # 12
"""
