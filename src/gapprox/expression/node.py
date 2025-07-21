# expression representation system for symbolic regression
# https://en.wikipedia.org/wiki/Directed_acyclic_graph

# nodes store inputs in a list, outputs in a set. edges are stored bi-directionally
# each node is capable of evaluation, which recursively calls its inputs

#import graphlib

class Node:
	def __init__(self, payload:any):
		self.inputs = list()
		self.payload = payload
		self.outputs = set()
	
	def evaluate(self, substitutions:dict=None):
		substitutions = substitutions or {}
		if callable(self.payload):
			return self.payload(*(input.evaluate(substitutions) for input in self.inputs))
		else:
			return substitutions.get(self.payload, self.payload)

	@staticmethod
	def connect(source:'Node', target:'Node', index:int):
		while len(target.inputs) <= index:
			target.inputs.append(None)
		if target.inputs[index]:
			raise Exception(f"target.inputs[{index}] is already {target.inputs[index]}")
		target.inputs[index] = source
		source.outputs.add(target)

	@staticmethod
	def disconnect(source:'Node', target:'Node', index:int):
		if len(target.inputs)<=index or target.inputs[index]!=source:
			raise Exception(f"target.inputs[{index}] does not have Node {source}")
		if target not in source.outputs:
			raise Exception(f"source.outputs does not have {target}")
		target.inputs[index] = None
		source.outputs.remove(target)

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
