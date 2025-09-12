# NOTE: this version of dag.py only allows .inputs to be a list. tensor support is too much, and not pragmatic/practical.

# this .py has a lot of comments because i find it hard to parse what every line means. its easier to read linguistically sometimes. 

# from graphlib import TopologicalSorter

# NOTE: we technically do not need an Edge class. but when we start to store metadata like complexity penalty as 'weight', we do. imagine this: exp(x) and sin(x) are cheap. low weight. easy to think about. but exp(sin(x)) is suddenly very hard to think about. its high weight. you cannot store this weight in either one of them. individually theyre cheap but together, theyre expensive. it can only be stored in some relation between the two, which is exactly what an Edge is.
# heres a re-explanation by AI:
# - an Edge class isn’t strictly required for a DAG of expressions.
# - but once we want to attach metadata (e.g. complexity penalties), it becomes essential.
# - consider exp(x) and sin(x): both are cheap individually (low weight).
# - but exp(sin(x)) is suddenly much more complex. this cost does not belong
# - to either node alone, but to the relation between them. that relation is an Edge.

# NOTE: we also do not allow InputNode to store callables, because in python, functions themselves can be passed as arguments. if we start telling InputNode to call its callable payload, then it will never have the chance to pass that function itself as an output. only the result of calling that function. thus something like rand() to generate a random number will be implemented not as an InputNode but as a FunctionNode. thus InputNode can store callables but will not call them, and FunctionNode can store *only* callables (or references to them) and will always call them

# NOTE: storing tensorial inputs is bad because it muddies up code to be near-unreadable. objects sometimes having attributes and sometimes not is horrifyingly torturing. it indents code unnecessarily for just an existence check/special case. this is bad. the less special cases, the simpler and the better. just sayin...

# for finding how many valid inputs or outputs a node has
from typing import Iterable
def count(stuff:Iterable, something:any=None) -> int:
	'count how many things are in stuff, excluding something'
	return sum(thing!=something for thing in stuff)

from .misc import int_to_str	# for printing object IDs
from abc import ABC	# to make Node an abstract class

DEFAULT_NODE_METADATA:dict = {'weight': 1, 'fixed':False}	# not actually used
DEFAULT_EDGE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_INPUTNODE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_FUNCTIONNODE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_OUTPUTNODE_METADATA:dict = {'weight': 1, 'fixed':False}

class Node(ABC):
	'base class for InputNode, FunctionNode, OutputNode'
	def __init__(self, payload:any, metadata:dict=DEFAULT_NODE_METADATA):
		self.payload:any = payload
		self.metadata:dict = DEFAULT_NODE_METADATA if metadata is None else metadata

class InputNode(Node):
	'a node that returns its payload upon substitution'
	
	def __init__(self, payload:any, metadata:dict=None):
		super().__init__(payload, DEFAULT_INPUTNODE_METADATA.copy() if metadata is None else metadata)
		self.outputs:set[Edge] = set()
	
	def substitute(
			self, 
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			node_cache               :dict = None, # for remembering which nodes have already been substituted
			*,
			caching                  :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:
		
		# initialize dicts
		inputnode_payload_subs = dict() if inputnode_payload_subs is None else inputnode_payload_subs
		node_subs = dict() if node_subs is None else node_subs
		if caching:
			node_cache = dict() if node_cache is None else node_cache
		
		# do node substitution
		if self in node_subs:
			return node_subs[self]

		# do cache substitution
		if caching and self in node_cache:
			return node_cache[self]
	
		# do payload substitution
		if self.payload in inputnode_payload_subs:
			payload = inputnode_payload_subs[self.payload]
		else:
			payload = self.payload
		
		# ending part
		result = payload

		if caching:
			node_cache[self] = result

		return result

	def __repr__(self):
		id_str = f"ID={int_to_str.int_to_str(id(self), int_to_str.KATAKANA)}"
		outputs_str = f"{count(self.outputs)} outputs"
		payload_str = f"payload={self.payload!r}"
		return f"<InputNode: {id_str}, {outputs_str}, {payload_str}>"

	def __str__(self):
		output = f"InputNode (ID={int_to_str.int_to_str(id(self), int_to_str.KATAKANA)})"
		output += f"\npayload : {self.payload!r}"
		output += f"\nmetadata: {type(self.metadata)} with length {len(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n    {repr(key).ljust(max_key_len)}: {value}"
		output += f"\noutputs : {type(self.outputs)}, count={count(self.outputs)}, length={len(self.outputs)}"
		for edge in self.outputs:
			output += f"\n    {edge!r}"
		return output
		
class FunctionNode(Node):
	'a node that represents a callable'
	def __init__(self, payload:any, metadata:dict=None):
		super().__init__(payload, DEFAULT_FUNCTIONNODE_METADATA.copy() if metadata is None else metadata)
		self.inputs:list[Edge] = list()
		self.outputs:set[Edge] = set()
		
	def substitute(
			self, 
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			node_cache               :dict = None, # for remembering which nodes have already been substituted
			*,
			caching                  :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:
		
		# initialize dicts
		functionnode_payload_subs = dict() if functionnode_payload_subs is None else inputnode_payload_subs
		node_subs = dict() if node_subs is None else node_subs
		if caching:
			node_cache = dict() if node_cache is None else node_cache
		
		# do node substitution
		if self in node_subs:
			return node_subs[self]

		# do cache substitution
		if caching and self in node_cache:
			return node_cache[self]
	
		# do payload substitution
		if self.payload in functionnode_payload_subs:
			payload = functionnode_payload_subs[self.payload]
		else:
			payload = self.payload

		if not callable(payload):
			raise ValueError("payload is not callable")
		
		# ending part
		args = list()
		for edge in self.inputs:
			args.append(edge.source.substitute(inputnode_payload_subs, functionnode_payload_subs, node_subs, node_cache, caching=caching))
		result = payload(*args)

		if caching:
			node_cache[self] = result

		return result

	def __repr__(self):
		id_str = f"ID={int_to_str.int_to_str(id(self),int_to_str.HAN)}"
		inputs_str = f"{count(self.inputs)} inputs"
		outputs_str = f"{count(self.outputs)} outputs"
		payload_str = f"payload={self.payload!r}"
		return f"<FunctionNode: {id_str}, {inputs_str}, {outputs_str}, {payload_str}>"
	
	def __str__(self):
		output = f"FunctionNode (ID={int_to_str.int_to_str(id(self), int_to_str.HAN)})"
		output += f"\npayload : {self.payload!r}"
		output += f"\nmetadata: {type(self.metadata)} with length {len(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n    {repr(key).ljust(max_key_len)}: {value}"
		output += f"\ninputs  : {type(self.inputs)}, count={count(self.inputs)}, length={len(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n    [{index}]: {edge!r}"
		output += f"\noutputs : {type(self.outputs)}, count={count(self.outputs)}, length={len(self.outputs)}"
		for edge in self.outputs:
			output += f"\n    {edge!r}"
		return output
	
class OutputNode(Node):
	'a node that only represents things that want to point to a Node. an expression wants to point to the root of an expression. this node is how you achieve that'
	def __init__(self, payload:any, metadata:dict=None):
		super().__init__(payload, DEFAULT_FUNCTIONNODE_METADATA.copy() if metadata is None else metadata)
		self.inputs:list[Edge] = [None]	# initialized because OutputNode should always have exactly one input
	
	def substitute(
			self, 
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			node_cache               :dict = None, # for remembering which nodes have already been substituted
			*,
			caching                  :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:

		# integrity check
		if len(self.inputs) != 1:
			raise ValueError("OutputNode accepts exactly one input")
		
		# initialize dicts
		node_subs = dict() if node_subs is None else node_subs
		if caching:
			node_cache = dict() if node_cache is None else node_cache
		
		# do node substitution
		if self in node_subs:
			return node_subs[self]

		# do cache substitution
		if caching and self in node_cache:
			return node_cache[self]
	
		# ending part
		result = self.inputs[0].source.substitute(inputnode_payload_subs, functionnode_payload_subs, node_subs, node_cache, caching=caching)

		if caching:
			node_cache[self] = result

		return result

	def __repr__(self):
		id_str = f"ID={int_to_str.int_to_str(id(self), int_to_str.HANGUL)}"
		inputs_str = f"{count(self.inputs)} inputs"
		payload_str = f"payload={self.payload!r}"
		return f"<OutputNode: {id_str}, {inputs_str}, {payload_str}>"
	
	def __str__(self):
		output = f"OutputNode (ID={int_to_str.int_to_str(id(self), int_to_str.HANGUL)})"
		output += f"\npayload : {self.payload!r}"
		output += f"\nmetadata: {type(self.metadata)}, count={count(self.metadata)}, length={len(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n    {repr(key).ljust(max_key_len)}: {value}"
		output += f"\ninputs  : {type(self.inputs)}, count={count(self.inputs)}, length={len(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n    [{index}]: {edge!r}"
		return output
	
class Edge:
	'holds a directional relationship between a source node and a target node'
	def __init__(self, source:Node, target:Node, index:int, metadata:dict=None):
		self.source  :Node = source
		self.target  :Node = target
		self.index   :int  = index
		self.metadata:dict = DEFAULT_EDGE_METADATA.copy() if metadata is None else metadata

	def __repr__(self):
		id_str = f"ID={int_to_str.int_to_str(id(self), int_to_str.GREEK)}"
		source_str = f"{self.source.payload!r}"
		target_str = f"{self.target.payload!r}"
		index_str = f"[{self.index}]"
		return f"<Edge: {id_str}, {source_str} → {target_str} @ {index_str}>"

	def __str__(self):
		output = f"Edge (ID={int_to_str.int_to_str(id(self), int_to_str.GREEK)})"
		output += f"\nsource  : {self.source!r}"
		output += f"\ntarget  : {self.target!r}"
		output += f"\nindex   : {self.index}"
		output += f"\nmetadata: {type(self.metadata)}, count={count(self.metadata)}, length={len(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n    {repr(key).ljust(max_key_len)}: {value}"
		return output

class Dag:
	'handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_inputnode, new_functionnode, new_outputnode, and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge'

	def __init__(
			self,
			inputnodes   :set[InputNode]    = None, 
			functionnodes:set[FunctionNode] = None, 
			outputnodes  :set[OutputNode]   = None, 
			edges        :set[Edge]         = None,
			*, 
			strict       :bool              = True,
			):
		self.inputnodes   :set[InputNode]    = inputnodes or set()
		self.functionnodes:set[FunctionNode] = functionnodes or set()
		self.outputnodes  :set[OutputNode]   = outputnodes or set()
		self.edges        :set[Edge]         = edges or set()
		self.strict       :bool              = strict
	
	def new_inputnode(self, payload:any, metadata:dict=None, *, strict:bool=None) -> InputNode:
		'create a new InputNode and add it. also return it'
		new_node = InputNode(payload, metadata)
		self.add_node(new_node, strict=self.strict if strict is None else strict)
		return new_node
	
	def new_functionnode(self, payload:any, metadata:dict=None, *, strict:bool=None) -> FunctionNode:
		'create a new FunctionNode and add it. also return it'
		new_node = FunctionNode(payload, metadata)
		self.add_node(new_node, strict=self.strict if strict is None else strict)
		return new_node
	
	def new_outputnode(self, payload:any, metadata:dict=None, *, strict:bool=None) -> OutputNode:
		'create a new OutputNode and add it. also return it'
		new_node = OutputNode(payload, metadata)
		self.add_node(new_node, strict=self.strict if strict is None else strict)
		return new_node

	def new_edge(self, source:Node, target:Node, index:int, metadata:dict=None, *, strict:bool=None) -> Edge:
		'create a new edge instance and add it. also return it'
		new_edge = Edge(source, target, index, metadata)
		self.add_edge(new_edge, strict=self.strict if strict is None else strict)
		return new_edge
	
	def add_edge(self, edge:Edge, *, strict:bool=None)->Edge:
		"""add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge, or its source or target are not known"""
		if (self.strict if strict is None else strict):
			if edge in self.edges:
				raise ValueError(f"edge already exists in Dag's edges")
			if edge in edge.source.outputs:
				raise ValueError(f"edge already exists in its source's outputs")
			if edge in edge.target.inputs:
				raise ValueError(f"edge already exists in its target's inputs")
			if isinstance(edge.source, OutputNode):
				raise ValueError(f"cannot route an OutputNode to a Node")
			if isinstance(edge.target, InputNode):
				raise ValueError(f"cannot route a Node to an InputNode")
			if edge.target not in self.functionnodes and edge.target not in self.outputnodes:
				raise ValueError(f"edge's target does not exist in functionnodes nor outputnodes. edge:{edge!r}, edge.target:{edge.target!r}")
			if edge.source not in self.inputnodes and edge.source not in self.functionnodes:
				raise ValueError(f"edge's source does not exist in inputnodes nor functionnodes. edge:{edge!r}, edge.source:{self.source!r}")

		# update set of edges
		self.edges.add(edge)

		# set target's input
		for i in range(edge.index - len(edge.target.inputs) + 1):
			edge.target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

		# set source's output
		edge.source.outputs.add(edge)

	def remove_edge(self, edge:Edge, *, strict:bool=None):
		"""remove an edge

		overloaded to accept:
		remove_edge(edge:Edge)
		remove_edge(source:Node, target:Node, index:int)
		"""
		
		if (self.strict if strict is None else strict):
			if edge not in self.edges:
				raise ValueError("edge not found in Dag's edges set")
			if edge not in edge.source.outputs:
				raise ValueError("edge not found in source's outputs")
			if edge not in edge.target.inputs:
				raise ValueError("edge not found in target's inputs")
			if edge.index >= len(edge.source.inputs):
				raise ValueError("source's inputs is not long enough")
			if edge.target.inputs[edge.index] != edge:	# we already know edge exists in target's inputs
				raise ValueError("edge exists at wrong index in target's inputs")
		
		# update set of edges
		self.edges.remove(edge)
		
		# set target's input 
		edge.target.inputs[edge.index] = None
		
		# set source's output
		edge.source.outputs.remove(edge)
	
	def add_node(self, node:Node, *, strict:bool=None)->Node:
		'add a node to the corresponding nodes set'
		if (self.strict if strict is None else strict):
			if node in self.inputnodes:
				raise ValueError("node already exists in Dag's inputnodes")
			if node in self.functionnodes:
				raise ValueError("node already exists in Dag's functionnodes")
			if node in self.outputnodes:
				raise ValueError("node already exists in Dag's outputnodes")
		
		match node:
			case InputNode():
				self.inputnodes.add(node)
			case FunctionNode():
				self.functionnodes.add(node)
			case OutputNode():
				self.outputnodes.add(node)
		
	def remove_node(self, node:Node, *, cascade:bool=None, strict:bool=None)->Node:
		'remove a node, and all corresponding edges if cascade=False is given as argument'

		if (self.strict if strict is None else strict):
			if node not in self.inputnodes or node not in self.functionnodes or node not in self.outputnodes:
				raise ValueError("node not found in DAG")

		if cascade:
			# remove input edges
			if hasattr(node, 'inputs'):
				for edge in node.inputs:
					remove_edge(edge)
	
			# remove output edges
			if hasattr(node, 'outputs'):
				for edge in node.outputs:
					remove_edge(edge)

		# remove from Dag's nodes set
		match node:
			case InputNode():
				self.inputnodes.remove(node)
			case FunctionNode():
				self.functionnodes.remove(node)
			case OutputNode():
				self.outputnodes.remove(node)

	def __repr__(self): 
		id_str = f"ID={int_to_str.int_to_str(id(self), int_to_str.LATIN)}"
		inputnodes_str = f"{count(self.inputnodes)} InputNode"
		functionnodes_str = f"{count(self.functionnodes)} FunctionNode"
		outputnodes_str = f"{len(self.outputnodes)} OutputNode"
		edges_str = f"{len(self.edges)} Edge"
		return f"<Dag: {id_str}, {inputnodes_str}, {functionnodes_str}, {outputnodes_str}, {edges_str}>"

	def __str__(self):
		output = f"Dag (ID={int_to_str.int_to_str(id(self), int_to_str.LATIN)})"
		output += f"\ninputnodes: {type(self.inputnodes)}, count={count(self.inputnodes)}, length={len(self.inputnodes)}"
		for node in self.inputnodes:
			output += '\n    ' + repr(node)
		output += f"\nfunctionnodes: {type(self.inputnodes)}, count={count(self.functionnodes)}, length={len(self.functionnodes)}"
		for node in self.functionnodes:
			output += '\n    ' + repr(node)
		output += f"\noutputnodes: {type(self.inputnodes)}, count={count(self.outputnodes)}, length={len(self.outputnodes)}"
		for node in self.outputnodes:
			output += '\n    ' + repr(node)
		output += f"\nedges: {type(self.inputnodes)}, count={count(self.edges)}, length={len(self.edges)}"
		for edge in self.edges:
			output += '\n    ' + repr(edge)
		return output
	
	@staticmethod
	def tree_view(node, prefix=""):
		print(f"{prefix}{node!r}")
		if hasattr(node, 'inputs'):
			for index, edge in enumerate(node.inputs):
				Dag.tree_view(edge.source, prefix + str(index).ljust(4, '-'))
	
	@staticmethod
	def topologial_sort(node:Node):
		"return a topologically sorted list of Node. uses python's native graphlib.TopologicalSorter"
		raise NotImplementedError("not made yet. its pretty hard to do")
	
# now theres a question of whether or not we should let OutputNode return a list of Edge or not. im erring towards only one input. but how will its .inputs look? just a list with one element? why not store the element directly? but that would violate the contract for a node's {inputs and outputs}-handling

# upon substitution, a FunctionNode returns only one answer. the result of its callable. why should an OutputNode suddenly return multiple answers? it should also return one answer, just like FunctionNode.

"""
# OperatorNode implies that we introduce a new Operator. Operator is different from a python callable (aka a function) in that it can participate in symbolic simplification. for example, the operator sub(a,b) can be symbolically manipulated into add(a,neg(b)). something like concat(a,b) is not even math-oriented, and thus has no symbolic manipulability, and thus is not an operator.

# NOTE: do not implement as a separate class!! implement as a property!! currently facing namespace explosion

# if implementing all these new classes, strip Node of many of its functionalities and divide them into its subclasses. 

# final note: Edge might also need to be subclassed. a Dag as a data structure need not hold a mass attribute. i have to find some abstraction of an Edge that warrants holding such metadata. thus i can subclass and name it accordingly. in other words, have Edge (has source, target, index), and have SomeEdgeNameIdk(Edge) (has mass (default 1))

this is all cool and all but after you also do all this, you should also condense Variable and Constant into a single Symbol class that stores two things: name:str and value:float|int|whatever. also remove the Expression class. all it does is hold a string. and also probably dont implement Operator

gapprox is currently facing a namespace explosion crisis, so minimize and reduce as much as possible. if a distinction changes how the class operates, its fair to make it into a separate class (whether a sibling or a subclass). if it only changes what it is, then just implement it as a property.
"""

