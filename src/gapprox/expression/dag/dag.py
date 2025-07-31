from .node import Node
from .edge import Edge

class Dag:
	'handles all DAG-related operations. it handles Nodes and Edges. you may either create new ones with new_node and new_edge or add with add_node and add_edge. you may remove with remove_node and remove_edge'

	def __init__(self, nodes:set[Node]=None, edges:set[Edge]=None):
		self.nodes = nodes or set()
		self.edges = edges or set()

	def new_node(self, payload:any):
		'create a new node instance and add it. also return it'
		node = Node(payload)
		self.add_node(node)
		return node

	def try_new_node(self, payload:any):
		'create a new node instance and add it. also return it'
		node = Node(payload)
		self.try_add_node(node)
		return node

	def new_edge(self, source:Node, target:Node, index:int):
		'create a new edge instance and add it. also return it'
		edge = Edge(source, target, index)
		self.add_edge(edge)
		return edge

	def try_new_edge(self, source:Node, target:Node, index:int):
		'create a new edge instance and add it. also return it'
		edge = Edge(source, target, index)
		self.try_add_edge(edge)
		return edge
	
	def add_node(self, node:Node):
		'add a node. raises an error if the node already exists'
		if node in self.nodes:
			raise ValueError(f"{node} already exists")
		self.nodes.add(node)

	def try_add_node(self, node:Node):
		'add a node. does not raise an error if the node already exists'
		self.nodes.add(node)

	def remove_node(self, node:Node):
		'remove a node, and all corresponding edges. raises an error if the node or its corresponding edges are not found'
		if node not in self.nodes:
			raise ValueError(f"{node} does not exist")
		self.nodes.remove(node)
		for edge in node.inputs+node.outputs:
			if edge not in self.edges:
				raise ValueError(f"{edge} does not exist")
			self.remove_edge(edge)
	
	def try_remove_node(self, node:Node):
		'remove a node, and all corresponding edges. does not raise an error if the node or its corresponding edges are not found'
		self.nodes.discard(node)
		for edge in node.inputs+node.outputs:
			self.discard_edge(edge)

	def add_edge(self, edge:Edge):
		'add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge'
		if edge in self.edges:
			raise ValueError(f"{edge} already exists")
		elif edge in edge.source.outputs:
			raise ValueError(f"{edge} already exists in its source's outputs")
		if len(edge.target.inputs)>edge.index:
			if edge.target.inputs[edge.index]!=None:
				raise ValueError(f"{edge.target.inputs[edge.index]} already exists in its target's input")
		self.edges.add(edge)
		edge.source.outputs.add(edge)
		while len(edge.target.inputs) <= edge.index:
			edge.target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

	def try_add_edge(self, edge:Edge):
		'add an edge and update its source and target to know that edge. does not raise an error if the edge already exists, or its source or target already know that edge'
		self.edges.add(edge)
		edge.source.outputs.add(edge)
		while len(edge.target.inputs) <= edge.index:
			target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

	def remove_edge(self, edge:Edge):
		'remove an edge and update its source and target to forget that edge. raises an error if the edge is not found, or its source or target do not know that edge'
		if edge not in self.edges:
			raise ValueError(f"{edge} does not exist")
		elif edge not in edge.source.outputs:
			raise ValueError(f"{edge} does not exist in its target's outputs")
		elif edge.target.inputs[edge.index] != edge:
			raise ValueError(f"{edge.target.inputs[edge.index]} is not {edge}")
		self.edges.remove(edge)
		edge.source.outputs.remove(edge)
		edge.target.inputs[edge.index] = None

	def try_remove_edge(self, edge:Edge):
		'remove an edge, and update its source and target to forget that edge. does not raise an error if the edge is not found, or its source or target do not know that edge'
		self.edges.discard(edge)
		edge.source.outputs.discard(edge)
		edge.target.inputs[edge.index] = None
