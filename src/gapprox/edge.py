from .node import Node

class Edge:
	'an edge of a directed acyclic graph. it stores source, target, and since inputs of a Node are positional, it also stores the position as index. these are immutable but other metadata such as weight are mutable. it is managed by gapprox.Dag'
	def __init__(self, source:Node, target:Node, index:int):
		self.source = source
		self.target = target
		self.index = index

	def __repr__(self):
		return f"<Edge(source={self.source!r}, target={self.target!r}, index={self.index!r})>"

	def __str__(self):
		return f"{self.source} -> {self.target} @ [{self.index}]"

	def __hash__(self):
		return id(self)

	def __eq__(self, other):
		return other is self

	def debug_summary(self):
		print(f"source: {self.source}")
		print(f"target: {self.target}")
		print(f"index : {self.index}")
