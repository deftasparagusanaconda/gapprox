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
