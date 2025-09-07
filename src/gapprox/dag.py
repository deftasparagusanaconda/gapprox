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

# NOTE: nodes indicate the dimensionality of their inputs tensor by the nesting depth. if a function takes only a single argument, it is a scalar function and its inputs should be `Edge`. if it takes multiple arguments, its a vectorial function, and its inputs should be `[Edge1, Edge2, …]`. a scalar function should not store its singular input as `[Edge]` as this implies a vector of length 1. lastly, a function that takes no arguments should not have a .inputs attribute at all.

from .symbol import Symbol	# for representing variables and constants
from .misc.op_on_tensor import op_on_tensor	# for iterating through tensor of inputs

from abc import ABC	# to make Node an abstract class

import inspect # for get_min_max_arity, to get function arity

# this was originally for OutputNode, when it required only one input
#def trimmed_len(lst):	# to get arguments list without trailing None elements
#	'find length of lst without any trailing None elements'
#	for i in range(len(lst) - 1, -1, -1):
#		if lst[i] is not None:
#			return i + 1
#	return 0

# for FunctionNode, to get the arity of a function
def get_arity(func:callable):
	'find the arity of a function. returns (min arity:int, max arity:int, variadic:bool)'
	sig = inspect.signature(func)
	min = 0
	max = 0
	variadic = False

	for param in sig.parameters.values():
		if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD):
			max += 1
			if param.default is inspect._empty:
				min += 1
		if param.kind == inspect.Parameter.VAR_POSITIONAL:
			variadic = True

	return min, max, variadic

from typing import Sequence
def tensor_get_element(tensor, index:Sequence[int]):
	'return the element of a tensor at the given index, because python lists dont support tensorial indexing like t[0,1]'
	for i in index:
		tensor = tensor[i]
	return tensor

def tensor_change_element(tensor, index:Sequence[int], new:any):
	'change the element of a tensor at the given index, because python lists dont support tensorial indexing like t[0,1]'
	if len(index) < 1:
		raise ValueError('len(index) must be >0')
	for i in index[:-1]:
		tensor = tensor[i]
	tensor[index[-1]] = new

class Node(ABC):
	'base class for InputNode, FunctionNode, OutputNode. it defines any metadata desirable for iterative optimization, and an extras list for any additional metadata the user may want to add'
	def __init__(self, weight:float=1, extras:list[any]=None):
		'defines any attributes specific to DAG evaluation'
		self.weight:float = weight
		self.extras:list[any] = None	# user-defined extra attributes
			
class InputNode(Node):
	'a node that returns its payload upon substitution. can even pass a callable as a payload'
	
	def __init__(self, payload, weight:float=1, extras:list[any]=None):
		super().__init__(weight, extras)
		self.payload:any = payload
		self.outputs:set[Edge] = set()
	
	def substitute(
			self, 
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			#node_cache               :dict = None, # for remembering which nodes have already been substituted
			#caching       :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#recursing     :bool = True,  # substitute recursively 
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:

		# initialize subs dicts
		node_subs              = node_subs or set()
		inputnode_payload_subs = inputnode_payload_subs or set()
		
		# use node substitution
		if self in node_subs:
			return node_subs[self]
	
		#if self in node_cache:
		#	return node_cache[self]
		
		# use inputnode payload substitution
		if self.payload in inputnode_payload_subs:
			payload = inputnode_payload_subs[self.payload]
		else:
			payload = self.payload
	
		result = payload
		#node_cache[self] = result
		return result
		
class FunctionNode(Node):
	'a node that always has a callable or a str that represents a callable (which should be replaced with an actual callable during substitution)'
	def __init__(self, payload, weight:float=1, extras:list[any]=None, min_arity:int=None, max_arity:int=None, is_variadic:bool=None):
		'since python functions only take a vector shape of function arguments, inputs is either a single Edge or a list of Edge. if the callable has '
		super().__init__(weight, extras)
		self.payload:any = payload
		self.outputs:set[Edge] = set()
		self.is_variadic:bool

		if callable(payload):
			a,b,c = get_arity(payload)
			min_arity = a if min_arity is None else min_arity
			max_arity = b if max_arity is None else max_arity
			is_variadic = c if is_variadic is None else is_variadic
		else:
			if min_arity is None or max_arity is None or is_variadic is None:
				raise ValueError('must give complete arity information to initialize FunctionNode')

		if max_arity == 0 and not is_variadic:
			return
		
		self.inputs:Edge|list[Edge] = [None] * max_arity	# because dynamically changing list length later is expensive
		
	def substitute(
			self, 
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			#node_cache               :dict = None, # for remembering which nodes have already been substituted
			#caching       :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#recursing     :bool = True,  # substitute recursively 
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:
		'unfortunately, python functions only take vectorial input of arguments so FunctionNode allows only vectorial inputs list'

		# initialize subs dicts
		node_subs                 = node_subs or set()
		functionnode_payload_subs = functionnode_payload_subs or set()
		
		# use node substitution
		if self in node_subs:
			return node_subs[self]

		#if self in node_cache:
		#	return node_cache[self]
		
		# use functionnode payload substitution
		if self.payload in functionnode_payload_subs:
			payload = functionnode_payload_subs[self.payload]
		else:
			payload = self.payload
		
		# check if payload is not callable
		if not callable(payload):
			raise ValueError("payload is not callable!")
		
		# get arguments to call payload with
		args = (edge.source.substitute(node_subs, inputnode_payload_subs, functionnode_payload_subs) for edge in self.inputs)
		
		result = self.payload(*args)
		
		#node_cache[self] = result
		return result

class OutputNode(Node):
	"""a node that only represents things that want to point to a Node. an expression wants to point to the root of an expression. this node is how you achieve that.
		
	OutputNode technically need not store a payload, but it is useful nontheless for marking purposes. also does not technically need to store more than one input but does so anyway, storing inputs nodes in a tensor. thus the DAG supports tensors natively"""
	def __init__(self, weight:float=1, extras:list[any]=None):
		super().__init__(weight, extras)
		self.inputs = list()	# a tensor of Edge. theres no way to natively type-hint a tensor in python
		
	def substitute(
			self, 
			node_subs                :dict = None, # for substituting sub-trees or sub-expressions
			inputnode_payload_subs   :dict = None, # for substituting variables and such
			functionnode_payload_subs:dict = None, # for substituting op names with the actual callables
			#node_cache               :dict = None, # for remembering which nodes have already been substituted
			#caching       :bool = True,  # enable saving to and reading from the cache dict, to reduce repeated computation
			#mutating      :bool = False, # makes substitutions permanent by replacing any nodes by their result
			#recursing     :bool = True,  # substitute recursively 
			#sorting       :bool = False  # perform a topological sort before doing recursive substitution
			) -> any:

		# initialize subs dicts
		node_subs = node_subs or set()
		
		# use node substitution
		if self in node_subs:
			return node_subs[self]

		#if self in node_cache:
		#	return node_cache[self]
		
		#if trimmed_len(self.inputs) != 1:
		#	raise ValueError("must have exactly one input")

		#result = self.inputs[0].source.substitute(node_subs, inputnode_payload_subs, functionnode_payload_subs, node_cache)

		# call substitute on each 
		result = op_on_tensor(self.inputs, lambda a: a.source.substitute(node_subs, inputnode_payload_subs, functionnode_payload_subs))

		#node_cache[self] = result
		return result

class Edge:
	"""holds a directional relationship between a source node and a target node

	specific to mathematical evaluation, it also stores the index of the input that it should connect to, because functions take ordered arguments. furthermore, this index capability is extended to allow storing not just its connection to one-dimensional vector of arguments, but an n-dimensional tensor. this is done by making the index a list of ints, not just an int. using one int, we can represent a one-dimensional arguments vector. using n ints, we can represent an n-dimensional arguments tensor
	"""
	def __init__(self, source:Node, target:Node, index:tuple[int], weight:float=1):
		self.source:Node      = source
		self.target:Node      = target
		self.index :tuple[int] = index
		self.weight:float     = weight

	def pretty_print(self):
		print(f"source: {self.source}")
		print(f"target: {self.target}")
		print(f"index : {self.index}")
		print(f"weight: {self.weight}")

	def __repr__(self):
		return f"<Edge(source={self.source!r}, target={self.target!r}, index={self.index!r}, weight={self.weight!r})>"

	def __str__(self):
		return f"{self.source} -> {self.target} @ {self.index} (weight = {self.weight})"

	def __hash__(self):
		return id(self)

	def __eq__(self, other):
		return other is self

class Dag:
	'handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_node and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge'

	def __init__(
			self,
			inputnodes   :set[InputNode]    = None, 
			functionnodes:set[FunctionNode] = None, 
			outputnodes  :set[OutputNode]   = None, 
			edges        :set[Edge]         = None, 
			*, 
			strict       :bool              = True
			):
		self.inputnodes   :set[InputNode]    = inputnodes or set()
		self.functionnodes:set[FunctionNode] = functionnodes or set()
		self.outputnodes  :set[OutputNode]   = outputnodes or set()
		self.edges        :set[Edge]         = edges or set()
		self.strict       :bool              = strict
	
	def new_inputnode(self, payload)->InputNode:
		'create a new InputNode and add it. also return it'
		return self.add_node(InputNode(payload))
	
	def new_functionnode(self, payload)->FunctionNode:
		'create a new FunctionNode and add it. also return it'
		return self.add_node(FunctionNode(payload))
	
	def new_outputnode(self, payload=None)->OutputNode:
		'create a new OutputNode and add it. also return it'
		return self.add_node(OutputNode(payload))

	def new_edge(self, source:Node, target:Node, index:None|int|list[int])->Edge:
		'create a new edge instance and add it. also return it'
		return self.add_edge(Edge(source, target, index))
	
	def add_node(self, node:Node)->Node:
		'add an InputNode. raises an error if the node already exists. also return it'
#		if node in self.inputnodes and self.strict:
#			raise ValueError(f"{node} already exists")
		match node:
			case InputNode():
				self.inputnodes.add(node)
			case FunctionNode():
				self.functionnodes.add(node)
			case OutputNode():
				self.outputnodes.add(node)
		return node
	
	def remove_node(self, node:Node)->Node:
		'remove a node, and all corresponding edges. raises an error if the node or its corresponding edges are not found. also return it'

		if self.strict:
			raise NotImplementedError

		if isinstance(node, (FunctionNode, OutputNode)):
			for input_edge in node.inputs:
				self.edges.discard(input_edge)
				input_edge.source.outputs.discard(input_edge)
		if isinstance(node, (InputNode, FunctionNode)):
			for output_edge in node.outputs:
				self.edges.discard(output_edge)
				if len(edge.index) == 0:
					output_edge.target.inputs = []
				else:
					tensor_change_element(output_edge.target.inputs, edge.index, None)
		match node:
			case InputNode():
				self.inputnodes.discard(node)
			case FunctionNode():
				self.functionnodes.discard(node)
			case OutputNode():
				self.outputnodes.discard(node)
	"""
		if not self.strict:
			for edge in list(node.inputs) + node.outputs:
				self.discard_edge(edge)
			self.nodes.discard(node)
			self.input_nodes.discard(node)
			self.output_nodes.discard(node)
			return node
		if node not in self.nodes:
			raise ValueError(f"{node} does not exist")
		for edge in list(node.inputs) + node.outputs:
			if edge not in self.edges:
				raise ValueError(f"{edge} does not exist")
		for edge in list(node.inputs) + node.outputs:
			self.remove_edge(edge)
		self.nodes.remove(node)
		return node
	"""
	
	def add_edge(self, edge:Edge)->Edge:
		'add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge. also return it'
		if self.strict:
			if edge in self.edges:
				raise ValueError(f"{edge} already exists")
			elif edge in edge.source.outputs:
				raise ValueError(f"{edge} already exists in its source's outputs")
#			if len(edge.target.inputs) > edge.index:
#				if edge.target.inputs[edge.index]!=None:
#					raise ValueError(f"{edge.target.inputs[edge.index]} already exists in its target's input")
		# update set of edges
		self.edges.add(edge)

		# set source's output
		edge.source.outputs.add(edge)

		# set target's input
		if len(edge.index) == 0:
			edge.target.inputs = edge
		else:
			tensor_change_element(edge.target.inputs, edge.index, edge)

		return edge
	"""
	def remove_edge(self, edge:Edge)->Edge:
		'remove an edge and update its source and target to forget that edge. raises an error if the edge is not found, or its source or target do not know that edge. also return it'
		if not self.strict:
			self.edges.discard(edge)
			edge.source.outputs.discard(edge)
			edge.target.inputs[edge.index] = None
			return edge
		if edge not in self.edges:
			raise ValueError(f"{edge} does not exist")
		elif edge not in edge.source.outputs:
			raise ValueError(f"{edge} does not exist in its target's outputs")
		elif edge.target.inputs[edge.index] != edge:
			raise ValueError(f"{edge.target.inputs[edge.index]} is not {edge}")
		self.edges.remove(edge)
		edge.source.outputs.remove(edge)
		edge.target.inputs[edge.index] = None
		return edge
	"""
	@staticmethod
	def tree_view(node, prefix=""):
		print(f"{prefix}{node}")
		if hasattr(node, 'inputs'):
			if isinstance(node.inputs, Edge):
				Dag.tree_view(node.inputs.source, prefix + "|-")
			else:
				for edge in node.inputs:
					Dag.tree_view(edge.source, prefix + "|-")
	
	def pretty_print(self):
		'print a summary of all nodes, edges, and structure of the DAG'
		from os import get_terminal_size
		
		rows, cols = 80, 24
		
		print(' gapprox.Dag().pretty_print() '.center(rows, '─'))
		print()
		print(f"   InputNode count : {len(self.inputnodes)}")
		print(f"FunctionNode count : {len(self.functionnodes)}")
		print(f"  OutputNode count : {len(self.outputnodes)}")
		print(f"        Edge count : {len(self.edges)}")
		print(f"            strict : {self.strict}")
		print()
		print('tree view '.ljust(rows//2, '─'))
		print()
		for output_node in self.outputnodes:
			self.tree_view(output_node)
			print()
		print('InputNode '.ljust(rows//2, '─'))
		print()
		for node in self.inputnodes:
			node.pretty_print()
			print()
		print('FunctionNode '.ljust(rows//2, '─'))
		print()
		for node in self.functionnodes:
			node.pretty_print()
			print()
		print('OutputNode '.ljust(rows//2, '─'))
		print()
		for node in self.outputnodes:
			node.pretty_print()
			print()
		print('edges '.ljust(rows//2, '─'))
		print()
		for edge in self.edges:
			edge.pretty_print()
			print()
		print(' have a nice day :) '.center(rows, '─'))
	
	def __repr__(self): return f"<gapprox.Dag() at {hex(id(self))}>"


"""
# OperatorNode implies that we introduce a new Operator. Operator is different from a python callable (aka a function) in that it can participate in symbolic simplification. for example, the operator sub(a,b) can be symbolically manipulated into add(a,neg(b)). something like concat(a,b) is not even math-oriented, and thus has no symbolic manipulability, and thus is not an operator.

# NOTE: do not implement as a separate class!! implement as a property!! currently facing namespace explosion

# if implementing all these new classes, strip Node of many of its functionalities and divide them into its subclasses. 

# final note: Edge might also need to be subclassed. a Dag as a data structure need not hold a mass attribute. i have to find some abstraction of an Edge that warrants holding such metadata. thus i can subclass and name it accordingly. in other words, have Edge (has source, target, index), and have SomeEdgeNameIdk(Edge) (has mass (default 1))

this is all cool and all but after you also do all this, you should also condense Variable and Constant into a single Symbol class that stores two things: name:str and value:float|int|whatever. also remove the Expression class. all it does is hold a string. and also probably dont implement Operator

gapprox is currently facing a namespace explosion crisis, so minimize and reduce as much as possible. if a distinction changes how the class operates, its fair to make it into a separate class (whether a sibling or a subclass). if it only changes what it is, then just implement it as a property.
"""

"""
    def __repr__(self):
        return f"<Node(payload={self.payload!r}, mass={self.mass!r}, inputs={self.inputs}, outputs={self.outputs})>"

    def __str__(self):
        return str(self.payload)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return other is self

    def pretty_print(self):
        print(f"payload  : {self.payload!r}")
        print(f"mass     : {self.mass!r}")
        if len(self.inputs) == 0:
            print(f"inputs   : []")
        else:
            for index, input in enumerate(self.inputs):
                print(f"inputs[{index}]: {input}")
        if len(self.outputs) == 0:
            print(f"outputs  : set()")
        else:
            for output in self.outputs:
                print(f"outputs  : {output}")
"""
