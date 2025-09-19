import gapprox

class Node:
	'a node of a directed acyclic graph. it holds a string as a payload. the meaning of the string is decoded using a context dict'
	def __init__(self, payload: str):
		self.payload: str = payload
		self.inputs: list['Edge'] = list()
		self.outputs: set['Edge'] = set()

	def __repr__(self):
		return f"<Node at {hex(id(self))}: {len(self.inputs)} inputs, {len(self.outputs)} outputs, payload={self.payload!r}>"

	def __str__(self):
		output = f"Node at {hex(id(self))}"
		output += f"\n    payload: {payload!r}"
		output += f"\n    inputs: {type(inputs)}, len={len(self.inputs)}"
		for index, edge in enumerate(self.inputs):
			output += f"\n        [index]: {edge!r}"
		output += f"\n    outputs: {type(outputs)}, len={len(self.outputs)}"
		for edge in self.outputs:
			output += f"\n        {edge!r}"
		return output

class Edge:
	"an edge of a directed acyclic graph. it connects two nodes together, with a special 'index' attribute, that denotes 'at what index' of the inputs it is connecting to"
	def __init__(self, source: Node, target: Node, index: int):
		self.source: Node = source
		self.target: Node = target
		self.index: int = index

	def __repr__(self):
		return f"<Edge at {hex(id(self))}: {self.source.payload} → {self.target.payload} @ [{index}]>"

	def __str__(self):
		output = f"Edge at {hex(id(self))}"
		output += f"\n    source: {self.source!r}"
		output += f"\n    target: {self.target!r}"
		output += f"\n    index : {self.index!r}"
		return output

class Dag:
	"""handles all DAG-related operations. it handles Nodes and Edges. you may create new ones with new_node and new_edge, add with add_node and add_edge, remove with remove_node and remove_edge

	a Dag prefers not to have two separate sub-graphs. it prefers that all nodes be connected, and that there are no
	↪orphan nodes. this is not enforced in code anywhere, but its the best design choice. if you want to have two
	↪separate subgraphs, create two separate Dag instances
	"""

	def __init__(self, *, nodes: set[Node] = None, edges: set[Edge] = None):
		self.nodes: set[Node] = set() if nodes is None else nodes
		self.edges: set[Edge] = set() if edges is None else edges

	def new_node(self, payload: str) -> Node:
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
		for i in range(edge.index - len(edge.target.inputs) + 1):
			edge.target.inputs.append(None)
		edge.target.inputs[edge.index] = edge

		# set source's output
		edge.source.outputs.add(edge)

	def remove_edge(self, edge: Edge) -> None:
		"""remove an edge. if gapprox.debug is True, it performs local structure integrity checks"""

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

		if gapprox.debug:
			if node not in self.nodes:
				raise ValueError("node not found in Dag")

		# remove edges
		for edge in node.inputs | node.outputs:
			self.remove_edge(edge)

		# update nodes set
		self.nodes.remove(node)

	def __repr__(self):
		return f"<Dag at {hex(id(self))}: {len(self.nodes)} nodes, {len(self.edges)} edges>"

	def __str__(self):
		output = f"Dag at {hex(id(self))}"
		output += f"\n    nodes: {type(self.nodes)}, len={len(self.nodes)}"
		for node in self.nodes:
			output += f"\n        {node!r}"
		output += f"\n    edges: {type(self.edges)}, len={len(self.edges)}"
		for edge in self.edges:
			output += f"\n        {edge!r}"
		return output

	@staticmethod
	def print_tree_view(node, prefix :str = ''):
		print(prefix + repr(node))
		for index, edge in enumerate(node.inputs):
			Dag.tree_view(edge.source, prefix + str(index).ljust(4, '-'))
