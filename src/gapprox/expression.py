from .dag import Node, Dag
from .operator_dict import operator_dict

class Expression:
	'represents a mathematical expression. it is evaluable and callable. the canonical storage is as a DAG, because it reveals the most structure about a math expression.'
		
	def __init__(self, dag: Dag, root: Node, context: dict[str, any] = operator_dict):
		if root.payload is not None:
			raise ValueError("expected root node to have payload=None")
		self.dag: Dag = dag
		self.root: Node = root
		self.context: dict[str, any] = context
		
	def evaluate(self, **kwargs):
		'allows evaluation of the expression using a substitution dict'
		
		context: dict[str, any] = self.context.copy()
		context.update(kwargs)

		def evaluate_node(node: Node) -> any:
			if len(node.inputs) == 0:
				return context[node.payload] if isinstance(node.payload, str) else node.payload
			else:
				function = context[node.payload] if isinstance(node.payload, str) else node.payload
				arguments = (evaluate_node(edge.source) for edge in node.inputs)
				return function(*arguments)

		return evaluate_node(self.root.inputs[0].source)

	__call__ = evaluate # makes the expression callable

	def __repr__(self):
		return f"<Expression at {hex(id(self))}: dag={self.dag!r}, {len(self.context)} contexts>"

	def __str__(self):
		output = f"Expression at {hex(id(self))}"
		output += f"\n    dag: {self.dag!r}"
		output += f"\n    context: {type(self.context)}, len={len(self.context)}"
		for key, value in self.context.items():
			output += f"\n        {key!r}: {value!r}"
		return output
