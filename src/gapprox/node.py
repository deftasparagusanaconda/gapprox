# from graphlib import TopologicalSorter

class Node:
	'a node of a directed acyclic graph (DAG). it can store local edges for quick local traversal. payload is immutable but inputs and outputs are mutable. it is managed by gapprox.Dag'
	
	def __init__(self, payload:any, mass:float=1):
		self.payload:any = payload
		self.mass:float = mass
		self.inputs:list['Edge'] = list()
		self.outputs:set['Edge'] = set()

	def substitute(self, substitutions:dict={}):
		"""perform a cached recursive DFS substitution with a dict. a python dict is passed by reference so it need not return updates through arguments.

		if you need the resulting substitution dict, initialize a dict and pass it instead of relying on the function's default one. the dict you made will hold all the substitutions you want :) <3!"""
		if self in substitutions:
			return substitutions[self]
		
		elif any(True for input in self.inputs if input is not None):
			arguments = list()
			for input in self.inputs:
				if input is None:
					arguments.append(None)
				else:
					arguments.append(input.source.substitute(substitutions))
			result = self.payload(*arguments)
		
		else:
			result = substitutions.get(self.payload, self.payload)

		substitutions[self] = result
		return result
	"""
	def is_input(self):
		return len(self.inputs) == 0

	def is_branch(self):
		return len(self.inputs)!=0 and len(self.outputs)!=0

	def is_output(self):
		return len(self.outputs) == 0
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
subclassing plan:

class Node:

class InputNode(Node):
	has outputs 

class MiddleNode(Node):
	has inputs
	has outputs

class OutputNode(Node):
	has inputs (PLURAL inputs. many inputs. not just one)

# these three subclasses are data-structure-level abstractions and the Dag should be specialized to work with these three types.
# a class with some particular properties can live as a normal class but once those properties start affecting the attributes, like not ever using an attribute, then it should probably be a subclass, and the superclass should be stripped from some of those attributes

---- in a separate file ... ----------

# these Node types are math-specific abstractions, not data-structure-level abstractions. and the Dag should not specialize to work with these.

class ConstantNode(InputNode)
	has payload (must be a Constant)
	has mass (default 1)

class VariableNode(InputNode)
	has payload (must be a Variable)
	has mass (default 1)

class FunctionNode(MiddleNode)
	has payload (must be a python callable. wrapping python's callables into a Function class is redundant)
	# (DOES NOT HAVE MASS)

class OperatorNode(FunctionNode)
	has payload (must be an Operator)
	has mass (default 1)

class ExpressionNode(OutputNode)
	has payload (must be an Expression)
	has mass (default 1)

# OperatorNode implies that we introduce a new Operator. Operator is different from a python callable (aka a function) in that it can participate in symbolic simplification. for example, the operator sub(a,b) can be symbolically manipulated into add(a,neg(b)). something like concat(a,b) is not even math-oriented, and thus has no symbolic manipulability, and thus is not an operator.

# if implementing all these new classes, strip Node of many of its functionalities and divide them into its subclasses. 

# final note: Edge might also need to be subclassed. a Dag as a data structure need not hold a mass attribute. i have to find some abstraction of an Edge that warrants holding such metadata. thus i can subclass and name it accordingly. in other words, have Edge (has source, target, index), and have SomeEdgeNameIdk(Edge) (has mass (default 1))

"""
