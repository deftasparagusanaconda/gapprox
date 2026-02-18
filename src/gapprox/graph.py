class Node:
	'a node of a multi-edged directed graph'
	def __init__(self):
		self.inputs: set['Edge'] = set()
	
	def disconnect(self) -> None:
		while self.inputs:
			edge = self.inputs.pop()
			edge.source.outputs.remove(edge)
		# we use .remove instead of .discard because we want to be strict. if your edge isnt properly embedded in the graph, then you cant properly remove it. and so you catch errors earlier. defensive programming.. i suppose
	
	def tree_view(self, prefix: str = '') -> str:
		output = f'{prefix}{self!r}\n'
		for edge in self.inputs:
			output += edge.source.tree_view(prefix + '|---')
		return output

	def __repr__(self) -> str:
		return f"<Node at {hex(id(self))}: {len(self.inputs)} inputs>"

class Edge:
	'an edge of a multi-edged directed graph'
	def __init__(self, source: Node, target: Node):
		self._target = target

		self.source: Node = source
		self.target: Node = target
	
	@property
	def target(self) -> Node:
		return self._target
	
	@target.setter
	def target(self, node) -> None:
		self._target.inputs.remove(self)
		self._target = node
		node.inputs.add(self)
		
	def disconnect(self) -> None:
		self.target.inputs.remove(self)
		# we use .remove instead of .discard because we want to be strict. if your edge isnt properly embedded in the graph, then you cant properly remove it. and so you catch errors earlier. defensive programming.. i suppose

	def __repr__(self) -> str:
		return f"<Edge at {hex(id(self))}: {self.source!r} → {self.target!r}, payload = {self.payload!r}>"

'''
import gapprox

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
			'edge_index_validity'     : {edge: edge.index < len(edge.target.inputs) for edge in self.edges},
			'edge_source_non_rootness': {edge: not edge.source.is_root for edge in self.edges},
			'edge_target_non_leafness': {edge: not edge.target.is_leaf for edge in self.edges}}

	@property
	def holds_integrity(self) -> bool:
		return all(all(dictionary.values()) for dictionary in self.get_integrity_dict().values())
	
	def visualize(self, context:dict[str, dict[str, any]] = gapprox.default_context) -> None:
		try:
			import networkx as nx
			import matplotlib.pyplot as plt
		except ImportError:
			print('this method requires networkx and matplotlib to be installed')

		graph = nx.MultiDiGraph()

		# add nodes
		for node in self.nodes:
			graph.add_node(node)

		# add edges
		for edge in self.edges:
			graph.add_edge(edge.source, edge.target)

		# positions
		try:
			pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
		except:
			pos = nx.spring_layout(graph)  # fallback

		# draw
		plt.figure(figsize=(12, 8))
		labels = {node: context[node.metadata]['symbols'][0] if node.metadata in context and 'symbols' in context[node.metadata] else repr(node.metadata) for node in graph.nodes}
		nx.draw(graph, pos, with_labels=True, labels=labels, node_size=1200, arrowsize=20)

		plt.show()

	def __repr__(self) -> str:
		return f"<MultiDAG at {hex(id(self))}: {len(self.nodes)} nodes, {len(self.edges)} edges>"

	def __str__(self) -> str:
		output = f"MultiDAG at {hex(id(self))}:"
		output += f"\n    nodes: {type(self.nodes)}, len={len(self.nodes)}"
		for node in self.nodes:
			output += f"\n        {node!r}"
		output += f"\n    edges: {type(self.edges)}, len={len(self.edges)}"
		for edge in self.edges:
			output += f"\n        {edge!r}"
		return output

	@staticmethod
	def tree_view(node, prefix: str = '') -> str:
		output = f'{prefix}{node!r}\n'
		for index, edge in enumerate(node.inputs):
			output += MultiDAG.tree_view(edge.source, prefix + str(index).ljust(4, '-'))
		return output
'''

"""
from collections.abc import Sequence
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

class NodeVisitor:
	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

	base class for any node visitor
	"""
#	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

#	this class is really just a stateful function that traverses through nodes in a DAG. the difference is that it will have different logic for different kinds of nodes. you make a subclass of it, and there you define visit_* methods, where * is your node's class name. say you have ParameterNode. then you would define something like visit_ParameterNode and you would call MyNodeVisitorSubclass().visit(ParameterNode)

#	like ast.NodeVisitor, it defines visit and generic_visit, and subclasses are supposed to define visit_* (* meaning YourClassName)
#	unlike ast.NodeVisitor, it does not define generic_visit or visit_Constant, is not specific to a tree structure, and is not specific to ast nodes. it supports a directed acyclic graph data structure, and is generic to *any* kind of DAG node (i think). it also is not limited to root-to-leaf traversal, and can be bi-directional or such

#	for a tree structure, a node is visited once. for a DAG structure, a node may be visited multiple times. implement your own memoization if you do not want this repeated traversal.

#	to mutate nodes during traversal, use gapprox.NodeTransformer instead. NodeVisitor is only meant for read-only traversal

#	it is generally recommended to name any subclasses of NodeVisitor as *Visitor such as SubstitutionVisitor, StringifyVisitor, …
#	"""

	def visit(self, node) -> any:
		'the thing to call to start traversal. never start traversal by calling visit_*(mynode). always start traversal by calling visit(mynode)'

		method = 'visit_' + str(node.metadata)
		visitor = getattr(self, method, self.generic_visit)

		return visitor(node)

	def generic_visit(self, node) -> any:
		'generic_visit generally defines the method (pre-order or post-order) and the direction (towards root or toward leaves) of recursion'
		raise ValueError("this {self.__class__.__name__} got {node=}, {type(node)=} and no corresponding visit_* was defined")
	
	def __repr__(self):
		# all names in the instance
		all_names = dir(self)
		
		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods	= [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]
		
		name_str = self.__class__.__name__	# in case derived classes dont implement their own __repr__ which they probably wont
		attributes_str = f"{len(attributes)} attributes"
		methods_str = f"{len(methods)} methods"
		return f"<{name_str} at {hex(id(self))}: {attributes_str}, {methods_str}>"
		
	def __str__(self):
		from collections.abc import Iterable

		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods	= [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		output = f"{self.__class__.__name__} (ID={hex(id(self))})"
		output += f"\nattributes: {len(attributes)} defined"
		for name in attributes:
			value = getattr(self, name)
			if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
				output += f"\n	{name} = {type(value)}, len={len(value)}"
			else:
				output += f"\n	{name} = {value}"
		output += f"\nmethods: {len(methods)} defined"
		for method in methods:
			output += f"\n	{method}()"
		return output

