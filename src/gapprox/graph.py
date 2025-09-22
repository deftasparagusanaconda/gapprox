class Vertex:
	'a vertex of a graph. can hold metadata like payload, weight, etc'
	def __init__(self, metadata: any | None = None):
		self.metadata: any = None = metadata

class Walk:
	'a walk of a graph. stores a '
	def __init__(self, metadata: any | None = None):
		self.metadata: any | None = metadata
	
	@property
	def is_closed(self) -> bool:
		return 


class Trail(Walk):

class Path(Path):
	'a path of a graph. instead of an Edge, we use a Path so that we can represent n-ary relations. it holds a tuple of Node, or a tuple of Edge. the path can also hold metadata like weight'
	def __init__(self, metadata: any | None = None):
		self.metadata: any | None = metadata

class Graph:
	'an undirected simple graph. though a graph in the formal mathematical sense is defined as tuple[set[Node], set[Edge]], here we directly flatten the set of nodes and set of edges as .nodes and .edges attributes'
	def __init__(self, nodes: set[Node] = None, edges: set[Edge] = None):
		self.nodes: set[Node] = set() if nodes is None else nodes
		self.edges: set[Edge] = set() if edges is None else edges

import gapprox
from typing import Iterable
from .misc import count

class Node:
	'a node of a directed acyclic graph. it can hold anything as a payload.'
	def __init__(self, payload: any):
		self.payload: any = payload
		self.inputs: list['Edge'] = list()
		self.outputs: set['Edge'] = set()

	@property
	def is_root(self) -> bool:
		return len(self.outputs) == 0 and count(self.inputs) != 0

	@property
	def is_branch(self) -> bool:
		return len(self.outputs) != 0 and count(self.inputs) != 0
	
	@property
	def is_leaf(self) -> bool:
		return len(self.outputs) != 0 and count(self.inputs) == 0

	@property
	def is_orphan(self) -> bool:
		return len(self.outputs) == 0 and count(self.inputs) == 0

	def __repr__(self) -> str:
		return f"<Node at {hex(id(self))}: {count(self.inputs)} inputs, {len(self.outputs)} outputs, payload={self.payload!r}>"

	def __str__(self) -> str:
		output = f"Node at {hex(id(self))}"
		output += f"\n    payload: {self.payload!r}"
		output += f"\n    inputs: {type(self.inputs)}, len={len(self.inputs)}, count={count(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n        [index]: {edge!r}"
		output += f"\n    outputs: {type(self.outputs)}, len={len(self.outputs)}"
		for edge in self.outputs:
			output += f"\n        {edge!r}"
		return output

class Edge(Path):
	"an edge of a directed acyclic graph. it connects two nodes together, with a special 'index' attribute, that denotes 'at what index' of the inputs it is connecting to"
	def __init__(self, source: Node, target: Node, index: int):
		self.source: Node = source
		self.target: Node = target
		self.index: int = index

	def __repr__(self) -> str:
		return f"<Edge at {hex(id(self))}: {self.source.payload!r} → {self.target.payload!r} @ [{self.index}]>"

	def __str__(self) -> str:
		output = f"Edge at {hex(id(self))}"
		output += f"\n    source: {self.source!r}"
		output += f"\n    target: {self.target!r}"
		output += f"\n    index : {self.index!r}"
		return output

class Dag:
	"""handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_node and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge

	a Dag prefers not to have two separate sub-graphs. it prefers that all nodes be connected, and that there are no orphan nodes. this is not enforced in code anywhere, but its the best design choice. if you want to have two separate subgraphs, create two separate Dag instances

	a Dag will grow the inputs list of a Node when adding an Edge, but will not shrink it back
	"""

	def __init__(self, *, nodes: set[Node] = None, edges: set[Edge] = None):
		self.nodes: set[Node] = set() if nodes is None else nodes
		self.edges: set[Edge] = set() if edges is None else edges

	def new_node(self, payload: any) -> Node:
		'create a new Node and add it to the Dag. also return it'
		new_node = Node(payload)
		self.add_node(new_node)
		return new_node

	def new_edge(self, source: Node, target: Node, index: int) -> Edge:
		'create a new Edge and add it to the Dag. also return it'
		new_edge = Edge(source, target, index)
		self.add_edge(new_edge)
		return new_edge

	def add_edge(self, edge: Edge) -> None:
		"""add an edge and update its source and target to know that edge. if gapprox.debug is True, it performs local structural integrity checks"""
		if gapprox.debug:
			if edge in self.edges:
				raise ValueError("edge already exists in Dag's edges")
			if edge in edge.source.outputs:
				raise ValueError("edge already exists in its source's outputs")
			if edge in edge.target.inputs:
				raise ValueError("edge already exists in its target's inputs")
			if edge.source not in self.nodes:
				raise ValueError("edge's source not found in the Dag")
			if edge.target not in self.nodes:
				raise ValueError("edge's target not found in the Dag")

		# update set of edges
		self.edges.add(edge)

		# set target's input
		edge.target.inputs.extend([None]*((edge.index)-len(edge.target.inputs)+1))
		edge.target.inputs[edge.index] = edge

		# set source's output
		edge.source.outputs.add(edge)
	
	def remove_edge(self, edge: Edge) -> None:
		"""remove an edge. if gapprox.debug is True, it performs local structural integrity checks"""

		if gapprox.debug:
			if edge not in self.edges:
				raise ValueError("edge not found in Dag")
			if edge not in edge.source.outputs:
				raise ValueError("edge not found in source's outputs")
			if edge not in edge.target.inputs:
				raise ValueError("edge not found in target's inputs")
			if edge.index >= len(edge.source.inputs):
				raise ValueError("source's inputs is not long enough")
			if edge.target.inputs[edge.index] != edge:  # we already know edge exists in target's inputs
				raise ValueError("edge exists at wrong index in target's inputs")
			if edge.source.is_root:
				raise ValueError("edge holds a root node as source")

		# update set of edges
		self.edges.remove(edge)

		# set target's input
		edge.target.inputs[edge.index] = None

		# set source's output
		edge.source.outputs.remove(edge)

	def add_node(self, node: Node) -> None:
		'add a node to the Dag'
		if gapprox.debug and node in self.nodes:
			raise ValueError(f"{node!r} already exists in Dag's nodes")

		self.nodes.add(node)

	def remove_node(self, node: Node) -> None:
		'remove a node, and all corresponding edges'

		if gapprox.debug and node not in self.nodes:
			raise ValueError("node not found in Dag")

		# remove edges
		for edge in node.inputs | node.outputs:
			self.remove_edge(edge)

		# update nodes set
		self.nodes.remove(node)

	def get_integrity_dict(self) -> dict[str, dict[Node|Edge, bool]]:
		'return a dict[str, dict[Node|Edge, bool]] of integrity checks'
		return {
			'node_non_orphanage'      : {node: not node.is_orphan for node in self.nodes},
			'node_non_inputs_sparsity': {node: node.is_leaf or count(node.inputs)==len(node.inputs) for node in self.nodes},
			'node_inputs_belongness'  : {node: all(edge in self.edges for edge in node.inputs) for node in self.nodes},
			'node_outputs_belongness' : {node: all(edge in self.edges for edge in node.outputs) for node in self.nodes},
			'edge_source_belongness'  : {edge: edge.source in self.nodes for edge in self.edges},
			'edge_target_belongness'  : {edge: edge.target in self.nodes for edge in self.edges},
			'edge_index_validity'     : {edge: edge.index < len(edge.target.inputs) for edge in self.edges},
			'edge_source_non_rootness': {edge: not edge.source.is_root for edge in self.edges},
			'edge_target_non_leafness': {edge: not edge.target.is_leaf for edge in self.edges}}

	@property
	def holds_integrity(self) -> bool:
		return all(all(dictionary.values()) for dictionary in self.get_integrity_dict().values())
	
	def visualize(self) -> None:
		try:
			import networkx as nx
			import matplotlib.pyplot as plt
		except ImportError:
			print('this method required networkx and matplotlib to be installed')

		graph = nx.MultiDiGraph()

		# add nodes
		for node in self.nodes:
			graph.add_node(node)

		# add edges
		for edge in self.edges:
			graph.add_edge(edge.source, edge.target, index=edge.index)

		# positions
		try:
			pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
		except:
			pos = nx.spring_layout(graph)  # fallback

		# draw
		plt.figure(figsize=(12, 8))
		labels = {node: repr(node.payload) for node in graph.nodes}
		nx.draw(graph, pos, with_labels=True, labels=labels, node_size=1200, arrowsize=20)

		plt.show()

	def __repr__(self) -> str:
		return f"<Dag at {hex(id(self))}: {len(self.nodes)} nodes, {len(self.edges)} edges>"

	def __str__(self) -> str:
		output = f"Dag at {hex(id(self))}"
		output += f"\n    nodes: {type(self.nodes)}, len={len(self.nodes)}"
		for node in self.nodes:
			output += f"\n        {node!r}"
		output += f"\n    edges: {type(self.edges)}, len={len(self.edges)}"
		for edge in self.edges:
			output += f"\n        {edge!r}"
		return output

	@staticmethod
	def print_tree_view(node, prefix :str = '') -> None:
		print(prefix + repr(node))
		for index, edge in enumerate(node.inputs):
			Dag.print_tree_view(edge.source, prefix + str(index).ljust(4, '-'))
