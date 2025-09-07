from .node import Node
from .edge import Edge

class Dag:
	'handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_node and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge'

	def __init__(
			self, 
			nodes:set[Node]=None, 
			edges:set[Edge]=None, 
			input_nodes:set[Node]=None, 
			output_nodes:set[Node]=None, 
			*, 
			strict:bool=True):
		self.nodes:set[Node] = nodes or set()
		self.edges:set[Edge] = edges or set()
		self.input_nodes:set[Node] = input_nodes or set()      # nodes without inputs
		self.output_nodes:set[Node] = output_nodes or set()    # nodes without outputs
		self.strict:bool = strict

	@property
	def lonely_nodes(self)->set[Node]:
		'get a set of nodes which have neither inputs nor outputs. poor nodes :('
		return self.input_nodes.intersection(self.output_nodes)

	def new_node(self, payload:any)->Node:
		'create a new node instance and add it. also return it'
		return self.add_node(Node(payload))

	def new_edge(self, source:Node, target:Node, index:int)->Edge:
		'create a new edge instance and add it. also return it'
		return self.add_edge(Edge(source, target, index))

	def add_node(self, node:Node)->Node:
		'add a node. raises an error if the node already exists. also return it'
		if node in self.nodes and self.strict:
			raise ValueError(f"{node} already exists")
		self.nodes.add(node)
		self.input_nodes.add(node)
		self.output_nodes.add(node)
		return node

	def remove_node(self, node:Node)->Node:
		'remove a node, and all corresponding edges. raises an error if the node or its corresponding edges are not found. also return it'
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
		self.input_nodes.discard(node)
		self.output_nodes.discard(node)
		return node

	def add_edge(self, edge:Edge)->Edge:
		'add an edge and update its source and target to know that edge. raises an error if the edge already exists, or its source or target already know that edge. also return it'
		if self.strict:
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
		self.input_nodes.discard(edge.target)
		self.output_nodes.discard(edge.source)
		return edge

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
		if not edge.source.outputs:                       # Node stores outputs as a set
			self.output_nodes.add(edge.source)
		if all(e is None for e in edge.target.inputs):    # Node stores inputs as a list
			self.input_nodes.add(edge.target)
		return edge

	@staticmethod
	def tree_view(node, prefix=""):
		print(f"{prefix}{node}")
		for edge in node.inputs:
			Dag.tree_view(edge.source, prefix + "|-")
	
	def pretty_print(self):
		'print a summary of all nodes, edges, and structure of the DAG'
		from os import get_terminal_size

		rows, cols = get_terminal_size()

		print(' gapprox.Dag().pretty_print() '.center(rows, '-'))
		print()
		print(f"nodes       : {len(self.nodes)}")
		print(f"edges       : {len(self.edges)}")
		print(f"input nodes : {len(self.input_nodes)}")
		print(f"output nodes: {len(self.output_nodes)}")
		print(f"lonely nodes: {len(self.lonely_nodes)}")
		print(f"strict      : {self.strict}")
		print()
		print('tree view '.ljust(rows//2, '-'))
		print()
		for output_node in self.output_nodes:
			self.tree_view(output_node)
			print()
		print('nodes '.ljust(rows//2, '-'))
		print()
		for node in self.nodes:
			node.pretty_print()
			print()
		print('edges '.ljust(rows//2, '-'))
		print()
		for edge in self.edges:
			edge.pretty_print()
			print()
		print(' have a nice day :) '.center(rows, '-'))
	
	def __repr__(self): return f"<gapprox.Dag() at {hex(id(self))}>"
