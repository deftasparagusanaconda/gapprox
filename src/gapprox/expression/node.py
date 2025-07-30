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

