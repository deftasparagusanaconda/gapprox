from .misc import count
from collections.abc import Sequence
import gapprox

class Node:
	'a node of a MultiDAG. can hold metadata like metadata, weight, et cetera. also keeps track of adjacent edges on it directly, instead of putting that responsibillity to an adjacency list in MultiDiGraph'
	def __init__(self, metadata: ... = None, inputs: set['Edge'] = None, outputs: set['Edge'] = None):
		self.metadata: ... = metadata
		self.inputs: set['Edge'] = set() if inputs is None else inputs
		self.outputs: set['Edge'] = set() if outputs is None else outputs

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
		return f"<Node at {hex(id(self))}: {count(self.inputs)} inputs, {len(self.outputs)} outputs, metadata={self.metadata!r}>"

	def __str__(self) -> str:
		output = f"Node at {hex(id(self))}"
		output += f"\n    metadata: {self.metadata!r}"
		output += f"\n    inputs: {type(self.inputs)}, len={len(self.inputs)}, count={count(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n        [index]: {edge!r}"
		output += f"\n    outputs: {type(self.outputs)}, len={len(self.outputs)}"
		for edge in self.outputs:
			output += f"\n        {edge!r}"
		return output

class Edge:
	'a directed edge of a MultiDiGraph. can hold metadata'
	def __init__(self, source: Node, target: Node, metadata: ... = None):
		self.source: Node = source
		self.target: Node = target
		self.metadata: ... = metadata

class MultiDAG:
	'a multi-edged directed acyclic graph. it stores a set of Node and a set of Edge. it does not maintain an adjacency list. the nodes do that themselves'

	def __init__(self, *, nodes: set[Node] = None, edges:set[Edge] = None):
		self.nodes: set[Node] = set() if nodes is None else nodes
		self.edges: set[Edge] = set() if edges is None else edges
	
	@property
	def is_cyclic(self) -> bool:
		raise NotImplementedError

	def new_node(self, *args, **kwargs) -> Node:
		'create a new Node and add it to the MultiDAG. also return it'
		new_node = Node(*args, **kwargs)
		self.add_node(new_node)
		return new_node

	def new_edge(self, *args, **kwargs) -> Edge:
		'create a new Edge and add it to the MultiDAG. also return it'
		new_edge = Edge(*args, **kwargs)
		self.add_edge(new_edge)
		return new_edge

	def add_edge(self, edge: Edge) -> None:
		"""add an edge and update its source and target to know that edge. if gapprox.debug is True, it performs local structural integrity checks"""
		if gapprox.debug:
			if edge in self.edges:
				raise ValueError("edge already exists in MultiDAG's edges")
			if edge in edge.source.outputs:
				raise ValueError("edge already exists in its source's outputs")
			if edge in edge.target.inputs:
				raise ValueError("edge already exists in its target's inputs")
			if edge.source not in self.nodes:
				raise ValueError("edge's source not found in the MultiDAG")
			if edge.target not in self.nodes:
				raise ValueError("edge's target not found in the MultiDAG")

		# update set of edges
		self.edges.add(edge)

		# set target's input
		edge.target.inputs.add(edge)

		# set source's output
		edge.source.outputs.add(edge)
	
	def remove_edge(self, edge: Edge) -> None:
		"""remove an edge. if gapprox.debug is True, it performs local structural integrity checks"""

		if gapprox.debug:
			if edge not in self.edges:
				raise ValueError("edge not found in the MultiDAG")
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
		'add a node to the MultiDAG'
		if gapprox.debug and node in self.nodes:
			raise ValueError(f"{node!r} already exists in MultiDAG's nodes")

		self.nodes.add(node)

	def remove_node(self, node: Node) -> None:
		'remove a node, and all corresponding edges'

		if gapprox.debug and node not in self.nodes:
			raise ValueError("node not found in the MultiDAG")

		# remove edges
		for edge in node.inputs | node.outputs:
			self.remove_edge(edge)

		# update nodes set
		self.nodes.remove(node)

	def get_integrity_dict(self) -> dict[str, dict[Node|Edge, bool]]:
		'return a dict[str, dict[Node|Edge, bool]] of integrity checks'
		return {
			'node_non_orphanage'	  : {node: not node.is_orphan for node in self.nodes},
			'node_non_inputs_sparsity': {node: node.is_leaf or count(node.inputs)==len(node.inputs) for node in self.nodes},
			'node_inputs_belongness'  : {node: all(edge in self.edges for edge in node.inputs) for node in self.nodes},
			'node_outputs_belongness' : {node: all(edge in self.edges for edge in node.outputs) for node in self.nodes},
			'edge_source_belongness'  : {edge: edge.source in self.nodes for edge in self.edges},
			'edge_target_belongness'  : {edge: edge.target in self.nodes for edge in self.edges},
			'edge_index_validity'	 : {edge: edge.index < len(edge.target.inputs) for edge in self.edges},
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
		labels = {node: repr(node.metadata) for node in graph.nodes}
		nx.draw(graph, pos, with_labels=True, labels=labels, node_size=1200, arrowsize=20)

		plt.show()

	def __repr__(self) -> str:
		return f"<MultiDAG at {hex(id(self))}: {len(self.nodes)} nodes, {len(self.edges)} edges>"

	def __str__(self) -> str:
		output = f"MultiDAG at {hex(id(self))}"
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
			MultiDAG.print_tree_view(edge.source, prefix + str(index).ljust(4, '-'))

"""
class DiEdge:
	'a directed edge of a graph. can hold metadata'
	def __init__(self, source, target, metadata: ... = None):
		self.source: Node = source
		self.target: Node = target
		self.metadata: ... = metadata

class HyperEdge:
	'an undirected hyperedge of a hypergraph. same attribute shape as Edge but with different constructor. can hold metadata'
	def __init__(self, nodes: set[Node], metadata: ... = None):
		self.nodes: set[Node] = nodes
		self.metadata: ... = metadata

class HyperDiEdge:
	'a directed edge of a hypergraph. it can be used as a directed hyperedge, since it simply stores two set[Node]. can hold metadata like weight'
	edef __init__(self, sources: set[Node], targets: set[Node], metadata: ... = None):
		self.sources: set[Node] = sources
		self.targets: set[Node] = targets
		self.metadata: ... = metadata

class Walk:
	'a finite undirected walk of a graph. stores a sequence of node. can hold metadata'
	def __init__(self, nodes: Sequence[Node], metadata: ... = None):
		self.nodes: Sequence[Node] = nodes
		self.metadata: any | None = metadata
	
	@property
	def is_closed(self) -> bool:
		return self.nodes[0] == self.nodes[-1]

	@property
	def is_directed_trail(self) -> bool:
		'all implicit directed edges are distinct'
		seen: set[tuple[Node]] = set()
		return any((a, b) in seen or seen.add((a, b)) for a, b in zip(seq, seq[1:]))	# evil list comprehension mwhehehe

	@property
	def is_undirected_trail(self) -> bool:
		'all implicit undirected edges are distinct'
		seen: set[set[Node]] = set()
		return any({a, b} in seen or seen.add((a, b)) for a, b in zip(seq, seq[1:]))

	@property
	def is_path(self) -> bool:
		'all nodes are distinct'
		return len(set(self.nodes)) == len(self.nodes)

class Graph:
	'a graph. stores a set of Node and a set of Edge. it also maintains an adjacency dict[Node, set[Edge]]'
	def __init__(
			self, 
			nodes	 : set[Node] = None,
			edges	 : set[Edge] = None,
			*, 
			metadata  : ...	   = None):
		self.nodes: set[Node] = set() if nodes is None else nodes
		self.edges: set[Edge] = set() if edges is None else edges
		self.metadata  : ...	   = metadata

"""
