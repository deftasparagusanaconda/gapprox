from .count import count
from .symbol import Symbol
from .dag import InputNode, FunctionNode, OutputNode, Node, Edge, Dag
import gapprox

class NodeVisitor:
	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

	this class is really just a stateful function that traverses through nodes in a DAG. the difference is that it will have different logic for different kinds of nodes. you make a subclass of it, and there you define visit_* methods, where * is your node's class name. say you have ParameterNode. then you would define something like visit_ParameterNode and you would call MyNodeVisitorSubclass().visit(ParameterNode)

	like ast.NodeVisitor, it defines visit and generic_visit, and subclasses are supposed to define visit_* (* meaning YourClassName)
	unlike ast.NodeVisitor, it does not define generic_visit or visit_Constant, is not specific to a tree structure, and is not specific to ast nodes. it supports a directed acyclic graph data structure, and is generic to *any* kind of DAG node (i think). it also is not limited to root-to-leaf traversal, and can be bi-directional or such

	for a tree structure, a node is visited once. for a DAG structure, a node may be visited multiple times. implement your own memoization if you do not want this repeated traversal.

	to mutate nodes during traversal, use gapprox.NodeTransformer instead. NodeVisitor is only meant for read-only traversal

	it is generally recommended to name any subclasses of NodeVisitor as *Visitor such as SubstitutionVisitor, StringifyVisitor, …
	"""
	def visit(self, node):
		'the thing to call to start traversal. never start traversal by calling visit_SpecificNodeType(mynode). always start traversal using visit(mynode)'

		method = 'visit_' + node.__class__.__name__

		if hasattr(self, method):
			visitor = getattr(self, method)
		else:
			raise AttributeError(f"{method} not defined for {node!r}")

		return visitor(node)

	def __repr__(self):
		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods    = [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		name_str = self.__class__.__name__	# in case derived classes dont implement their own __repr__ which they probably wont
		attributes_str = f"{len(attributes)} attributes"
		methods_str = f"{len(methods)} methods"
		return f"<{name_str} at {hex(id(self))}: {attributes_str}, {methods_str}>"

	def __str__(self):
		from collections.abc import Iterable

		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods    = [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		output = f"{self.__class__.__name__} (ID={hex(id(self))})"
		output += f"\nattributes: {len(attributes)} defined"
		for name in attributes:
			value = getattr(self, name)
			if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
				output += f"\n    {name} = {type(value)}, count={count(value)}, length={len(value)}"
			else:
				output += f"\n    {name} = {value}"
		output += f"\nmethods: {len(methods)} defined"
		for method in methods:
			output += f"\n    {method}()"
		return output

class EvaluationVisitor(NodeVisitor):
	"""perform mathematical expression evaluation by returning InputNode payloads and calling FunctionNode payloads"""

	def __init__(self,
			inputnode_payload_subs   : dict = None, # for substituting variables and such
			functionnode_payload_subs: dict = None, # for substituting op names with the actual callables
			node_subs                : dict = None, # for substituting sub-trees or sub-expressions
			node_cache               : dict = None, # for remembering which nodes have already been substituted
			*,
			caching                  : bool = True, # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			):
		self.inputnode_payload_subs   : dict = dict() if inputnode_payload_subs    is None else inputnode_payload_subs
		self.functionnode_payload_subs: dict = dict() if functionnode_payload_subs is None else functionnode_payload_subs
		self.node_subs                : dict = dict() if node_subs                 is None else node_subs
		self.node_cache               : dict = dict() if node_cache                is None else node_cache
		self.caching                  : bool = caching
	
	def visit_InputNode(self, node: InputNode) -> any:
		# do node substitution
		if node in self.node_subs:
			return self.node_subs[node]
		
		# do cache substitution
		if self.caching and node in self.node_cache:
			return self.node_cache[node]
		
		# do payload substitution
		if node.payload in self.inputnode_payload_subs:
			payload = self.inputnode_payload_subs[node.payload]
		else:
			payload = node.payload

		# do symbol value substution
		if isinstance(payload, Symbol):
			payload = payload.value
		
		# ending part
		result = payload
		
		if self.caching:
			self.node_cache[node] = result
		
		return result

	def visit_FunctionNode(self, node: FunctionNode) -> any:
		# do node substitution
		if node in self.node_subs:
			return self.node_subs[node]

		# do cache substitution
		if self.caching and node in self.node_cache:
			return self.node_cache[node]

		# do payload substitution
		if node.payload in self.functionnode_payload_subs:
			payload = self.functionnode_payload_subs[node.payload]
		else:
			payload = node.payload

		if not callable(payload):
			raise ValueError(f"{payload!r} is not callable")

		# ending part
		args = list()
		for edge in node.inputs:
			args.append(self.visit(edge.source))
		result = payload(*args)

		if self.caching:
			self.node_cache[node] = result

		return result

	def visit_OutputNode(self, node: OutputNode) -> any:
		if gapprox.debug and len(node.inputs) != 1:
			raise ValueError("OutputNode accepts exactly one input")

		# do node substitution
		if node in self.node_subs:
			return self.node_subs[node]

		# do cache substitution
		if self.caching and node in self.node_cache:
			return self.node_cache[node]

		# ending part
		result = self.visit(node.inputs[0].source)

		if self.caching:
			self.node_cache[node] = result

		return result

class StringifyVisitor(NodeVisitor):
	"""turn a math expression DAG into a string
	"""
	pass

# make a class that can get the statistics of a spanning tree


