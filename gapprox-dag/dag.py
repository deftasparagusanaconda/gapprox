# expression representation system for symbolic regression
# https://en.wikipedia.org/wiki/Directed_acyclic_graph

# nodes store inputs in a list, outputs in a set. thus, edges are stored twice
# each node is capable of evaluation, which recursively calls its inputs
# multiple-output functions like divmod (return quotient & remainder) are not allowed

#boolean    = bool
#natural    = int
#whole      = int
#integer    = int
#rational   = float
#real       = float

#import graphlib
"""
from abc import ABC

class Node(ABC):
	# arbitrary class for InputNode, FunctinNode, OutputNode

	def __init__(self):
		...

	@abstractmethod
	def add_input(Node, index):
		...
	@abstractmethod
	def add_output(Node):
		...
	@abstractmethod
	def remove_input(Node, index):
		...
	@abstractmethod
	def remove_output(Node):
		...
	
	def evaluate(self, substitutions:dict):
		...
"""
class DAG:
	"""holds a set of nodes, which represent one graph"""

	def __init__(self, nodes=set()):
		self.nodes = nodes
	
	def add_node(self, node):
		self.nodes.add(node)
	
	def remove_node(self, node):
		self.nodes.remove(node)
	
	@staticmethod
	def connect(input, output, match=None):
		input.add_output(output)
		output.add_input(input, index)
	
	@staticmethod
	def disconnect(input, index=None, output):
		input.remove_output(output)
		output.remove_input(index)
	
	#def check_cyclicity(something):
	#def get_edge_list(self):
		# return a list of all edges enclosed by the DAG
		# edges that point to nodes outside the list are ignored

class NodeInput:
	"""holds a parameter (variable/constant/nullary function...) of a DAG
NodeInput has no inputs, but multiple outputs"""
	
	def __init__(self, value:any):
		self.outputs = set()
		self.value = value
	
	def add_output(self, output):
		self.outputs.add(output)

	def remove_output(self, output):
		self.outputs.remove(output)
	
	def evaluate(self, substitutions:dict=None):
		elif callable(self.value):
			return self.value()
		elif self.value in substitutions:
			return substitutions[self.value]
		return self.value

class NodeFunction:
	"""a function/operator node of a DAG
NodeFunction has inputs and outputs"""

	def __init__(self, function:callable):

		if not callable(function):
			raise TypeError(f"{function} is not callable")

		self.function:callable = function
		self.variadic:bool = False
		self.arity:int = 0

		self.args_POSITIONAL_ONLY:list = []
		self.args_POSITIONAL_OR_KEYWORD:list = []
		self.args_VAR_POSITIONAL:list = []
		self.args_KEYWORD_ONLY:dict = {}
		self.args_VAR_KEYWORD:dict = {}

		from inspect import signature
		params = signature(function).parameters.values()

		# check if it has *args
		for param in params if param.default is not param.empty:
			match param.kind:
				case param.POSITIONAL_ONLY:
					self.POSITIONAL_ONLY.append(param)
				case param.POSITIONAL_OR_KEYWORD:
					self.POSITIONAL_ONLY.append(param)
				case param.VAR_POSITIONAL:
					pass
				case param.KEYWORD_ONLY:
					self.KEYWORD_ONLY.append(param)
				case param.VAR_KEYWORD:
					pass
				case _:
					raise ValueError(f"NodeFunction constructor found strange parameter kind: {param.kind]")

			self.arity += 1

		if self.arity == 0 and self.variadic is False:
			raise ValueError(f"no-input functions not allowed. implement {function} as NodeInput instead")

		# count required positional args
		self.arity = len(p for p in params if p.kind is p.POSITIONAL_ONLY)

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
			args = 
			return self.function()
		else:
			raise ValueError("FunctionNode has no inputs")
# the grapher shall not show arguments that already had defaults

class NodeOutput:
	"""the root node of an expression. the grandpa of all nodes in an expression
NodeOutput has 1 input, no outputs"""

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
