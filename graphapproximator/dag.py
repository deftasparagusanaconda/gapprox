# expression representation system for symbolic regression
# https://en.wikipedia.org/wiki/Directed_acyclic_graph

# nodes also store their parents, children, and consequently, the edges of the graph
# each node is capable of evaluation like an isolated tree

import graphlib

class Node:	
	"""holds a node of a DAG representation of an expression"""
	def __init__(self):
		self.children:list[Node] = []
		self.parents:set[Node] = {}

class NodeParameter:
	"""holds a parameter (variable/constant/...) of a DAG"""

class NodeFunction:
	"""holds a function/operator of a DAG"""
	def __init__(self):
		self.parents:set[Node] = {}
		self.value = None
	def value(self):
		return self.value
