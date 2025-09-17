# NOTE: this version of dag.py only allows .inputs to be a list. tensor support is too much, and not pragmatic/practical.

# NOTE: we technically do not need an Edge class. but when we start to store metadata like complexity penalty as 'weight', we do. imagine this: exp(x) and sin(x) are cheap. low weight. easy to think about. but exp(sin(x)) is suddenly very hard to think about. its high weight. you cannot store this weight in either one of them. individually theyre cheap but together, theyre expensive. it can only be stored in some relation between the two, which is exactly what an Edge is.
# heres a re-explanation by AI:
# - an Edge class isn’t strictly required for a DAG of expressions.
# - but once we want to attach metadata (e.g. complexity penalties), it becomes essential.
# - consider exp(x) and sin(x): both are cheap individually (low weight).
# - but exp(sin(x)) is suddenly much more complex. this cost does not belong
# - to either node alone, but to the relation between them. that relation is an Edge.

# NOTE: OutputNode should not have any new special things going for it, like excluding payload, or excluding metadata because in other parts of the program, this causes more special cases just for this teeny tiny peeny piny little node that acts as a "pointer" in the DAG basically. so it has .inputs. but it also allows only one element to be stored in this one-element-long list

from .count import count	# for getting how many non-None elements are in something
from abc import ABC	# to make Node an abstract class
import gapprox	# for gapprox.debug:bool

DEFAULT_EDGE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_INPUTNODE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_FUNCTIONNODE_METADATA:dict = {'weight': 1, 'fixed':False}
DEFAULT_OUTPUTNODE_METADATA:dict = {'weight': 1, 'fixed':False}

class Node(ABC):
	'base class for InputNode, FunctionNode, OutputNode'
	def __init__(self, payload:any, metadata:dict):
		self.payload:any = payload
		self.metadata:dict = metadata

class InputNode(Node):
	'a leaf node'
	
	def __init__(self, payload:any, metadata:dict=None):
		super().__init__(payload, DEFAULT_INPUTNODE_METADATA.copy() if metadata is None else metadata)
		self.outputs:set[Edge] = set()
		
	def __repr__(self):
		outputs_str = f"{count(self.outputs)} outputs"
		payload_str = f"payload={self.payload!r}"
		return f"<InputNode at {hex(id(self))}: {outputs_str}, {payload_str}>"
		
	def __str__(self):
		output = f"InputNode at {hex(id(self))}:"
		output += f"\n    payload : {self.payload!r}"
		output += f"\n    metadata: {type(self.metadata)}, length={len(self.metadata)}, count={count(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n        {repr(key).ljust(max_key_len)}: {value}"
		output += f"\n    outputs : {type(self.outputs)}, length={len(self.outputs)}, count={count(self.outputs)}"
		for edge in self.outputs:
			output += f"\n        {edge!r}"
		return output
		
class FunctionNode(Node):
	'a branch node. its payload must be a callable, or something representing a callable, like a str'
	def __init__(self, payload:any, metadata:dict=None):
		super().__init__(payload, DEFAULT_FUNCTIONNODE_METADATA.copy() if metadata is None else metadata)
		self.inputs:list[Edge] = list()
		self.outputs:set[Edge] = set()

	def __repr__(self):
		inputs_str = f"{count(self.inputs)} inputs"
		outputs_str = f"{count(self.outputs)} outputs"
		payload_str = f"payload={self.payload!r}"
		return f"<FunctionNode at {hex(id(self))}: {inputs_str}, {outputs_str}, {payload_str}>"
	
	def __str__(self):
		output = f"FunctionNode at {hex(id(self))}:"
		output += f"\n    payload : {self.payload!r}"
		output += f"\n    metadata: {type(self.metadata)}, length={len(self.metadata)}, count={count(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n        {repr(key).ljust(max_key_len)}: {value}"
		output += f"\n    inputs  : {type(self.inputs)}, length={len(self.inputs)}, count={count(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n        [{index}]: {edge!r}"
		output += f"\n    outputs : {type(self.outputs)}, length={len(self.outputs)}, count={count(self.outputs)}"
		for edge in self.outputs:
			output += f"\n        {edge!r}"
		return output
	
class OutputNode(Node):
	'a root node. doesnt really hold any payload, nor does it need to. but you can. if you want to. :)'
	def __init__(self, payload:any=None, metadata:dict=None):
		super().__init__(payload, DEFAULT_FUNCTIONNODE_METADATA.copy() if metadata is None else metadata)
		self.inputs:list[Edge] = [None]	# initialized because OutputNode should always have exactly one input
	
	def __repr__(self):
		inputs_str = f"{count(self.inputs)} inputs"
		payload_str = f"payload={self.payload!r}"
		return f"<OutputNode at {hex(id(self))}: {inputs_str}, {payload_str}>"
	
	def __str__(self):
		output = f"OutputNode at {hex(id(self))}:"
		output += f"\n    payload : {self.payload!r}"
		output += f"\n    metadata: {type(self.metadata)}, length={len(self.metadata)}, count={count(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n        {repr(key).ljust(max_key_len)}: {value}"
		output += f"\n    inputs  : {type(self.inputs)}, length={len(self.inputs)}, count={count(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n        [{index}]: {edge!r}"
		return output
	
class Edge:
	'holds a directional relationship between a source node and a target node'
	def __init__(self, source:Node, target:Node, index:int, metadata:dict=None):
		self.source  :Node = source
		self.target  :Node = target
		self.index   :int  = index
		self.metadata:dict = DEFAULT_EDGE_METADATA.copy() if metadata is None else metadata

	def __repr__(self):
		source_str = f"{self.source.payload!r}"
		target_str = f"{self.target.payload!r}"
		index_str = f"[{self.index}]"
		return f"<Edge at {hex(id(self))}: {source_str} → {target_str} @ {index_str}>"

	def __str__(self):
		output = f"Edge at {hex(id(self))}):"
		output += f"\n    source  : {self.source!r}"
		output += f"\n    target  : {self.target!r}"
		output += f"\n    index   : {self.index}"
		output += f"\n    metadata: {type(self.metadata)}, length={len(self.metadata)}, count={count(self.metadata)}"
		max_key_len = max(len(repr(key)) for key in self.metadata.keys())
		for key, value in self.metadata.items():
			output += f"\n        {repr(key).ljust(max_key_len)}: {value}"
		return output

class Dag:
	"""handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_inputnode, new_functionnode, new_outputnode, and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge

	a Dag prefers not to have two separate sub-graphs. it prefers that all nodes be connected, and that there are no orphan nodes. this is not enforced in code anywhere, but its the best design choice. if you want to have two separate subgraphs, create two separate Dag instances
	"""

	def __init__(
			self,
			inputnodes   :set[InputNode]    = None, 
			functionnodes:set[FunctionNode] = None, 
			outputnodes  :set[OutputNode]   = None, 
			edges        :set[Edge]         = None,
			):
		self.inputnodes   :set[InputNode]    = inputnodes or set()
		self.functionnodes:set[FunctionNode] = functionnodes or set()
		self.outputnodes  :set[OutputNode]   = outputnodes or set()
		self.edges        :set[Edge]         = edges or set()
	
	def new_inputnode(self, payload:any, metadata:dict=None) -> InputNode:
		'create a new InputNode and add it. also return it'
		new_node = InputNode(payload, metadata)
		self.add_node(new_node)
		return new_node
	
	def new_functionnode(self, payload:any, metadata:dict=None) -> FunctionNode:
		'create a new FunctionNode and add it. also return it'
		new_node = FunctionNode(payload, metadata)
		self.add_node(new_node)
		return new_node
	
	def new_outputnode(self, payload:any=None, metadata:dict=None) -> OutputNode:
		'create a new OutputNode and add it. also return it'
		new_node = OutputNode(payload, metadata)
		self.add_node(new_node)
		return new_node

	def new_edge(self, source:Node, target:Node, index:int, metadata:dict=None) -> Edge:
		'create a new edge instance and add it. also return it'
		new_edge = Edge(source, target, index, metadata)
		self.add_edge(new_edge)
		return new_edge
	
	def add_edge(self, edge:Edge):
		"""add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge, or its source or target are not known"""
		if gapprox.debug:
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

	def remove_edge(self, edge:Edge):
		"""remove an edge
		"""

		if gapprox.debug:
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
	
	def add_node(self, node:Node):
		'add a node to the corresponding nodes set'
		if gapprox.debug:
			if node in self.inputnodes:
				raise ValueError(f"{node!r} already exists in Dag's inputnodes")
			if node in self.functionnodes:
				raise ValueError(f"{node!r} already exists in Dag's functionnodes")
			if node in self.outputnodes:
				raise ValueError(f"{node!r} already exists in Dag's outputnodes")
		
		match node:
			case InputNode():
				self.inputnodes.add(node)
			case FunctionNode():
				self.functionnodes.add(node)
			case OutputNode():
				self.outputnodes.add(node)
		
	def remove_node(self, node:Node):
		'remove a node, and all corresponding edges if cascade=False is given as argument'

		if gapprox.debug:
			if node not in self.inputnodes and node not in self.functionnodes and node not in self.outputnodes:
				raise ValueError("node not found in DAG")

		# remove input edges
		if hasattr(node, 'inputs'):
			for edge in node.inputs:
				self.remove_edge(edge)

		# remove output edges
		if hasattr(node, 'outputs'):
			for edge in node.outputs:
				self.remove_edge(edge)

		# remove from Dag's nodes set
		match node:
			case InputNode():
				self.inputnodes.remove(node)
			case FunctionNode():
				self.functionnodes.remove(node)
			case OutputNode():
				self.outputnodes.remove(node)
	
	def __repr__(self): 
		inputnodes_str = f"{count(self.inputnodes)} InputNode"
		functionnodes_str = f"{count(self.functionnodes)} FunctionNode"
		outputnodes_str = f"{len(self.outputnodes)} OutputNode"
		edges_str = f"{len(self.edges)} Edge"
		return f"<Dag at {hex(id(self))}: {inputnodes_str}, {functionnodes_str}, {outputnodes_str}, {edges_str}>"
	
	def __str__(self):
		output = f"Dag at {hex(id(self))}"
		output += f"\n    inputnodes: {type(self.inputnodes)}, length={len(self.inputnodes)}, count={count(self.inputnodes)}"
		for node in self.inputnodes:
			output += '\n        ' + repr(node)
		output += f"\n    functionnodes: {type(self.inputnodes)}, length={len(self.functionnodes)}, count={count(self.functionnodes)}"
		for node in self.functionnodes:
			output += '\n        ' + repr(node)
		output += f"\n    outputnodes: {type(self.inputnodes)}, length={len(self.outputnodes)}, count={count(self.outputnodes)}"
		for node in self.outputnodes:
			output += '\n        ' + repr(node)
		output += f"\n    edges: {type(self.inputnodes)}, length={len(self.edges)}, count={count(self.edges)}"
		for edge in self.edges:
			output += '\n        ' + repr(edge)
		return output
	
	@staticmethod
	def tree_view(node, prefix=""):
		print(f"{prefix}{node!r}")
		if hasattr(node, 'inputs'):
			for index, edge in enumerate(node.inputs):
				Dag.tree_view(edge.source, prefix + str(index).ljust(4, '-'))

# OperatorNode implies that we introduce a new Operator. Operator is different from a python callable (aka a function) in that it can participate in symbolic simplification. for example, the operator sub(a,b) can be symbolically manipulated into add(a,neg(b)). something like concat(a,b) is not even math-oriented, and thus has no symbolic manipulability, and thus is not an operator
