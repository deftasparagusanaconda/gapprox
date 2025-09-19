from .dag import Dag

class Expression:
	'represents a mathematical expression. it is evaluable and callable'

	def __init__(self, expression: str|Dag, context: dict[str, any]):
		self.expression: str|Dag = expression
		self.context: dict[str, any] = context

	def evaluate(self):
		raise ValueError("not made yet")

	__call__ = evaluate # makes the expression callable, like myexpr(2, 3)

	def __repr__(self):
		return f"<Expression at {hex(id(self))}: expression={self.expression!r}, {len(self.context)} contexts>"

	def __str___(self):
		output = "Expression at {hex(id(self))}"
		output += f"\nexpression: {self.expression!r}"
		output += f"\ncontext: {type(self.context)}, len={len(self.context)}"
		for key, value in self.context.items():
			output += f"\n{key!r}: {value!r}"
		return output
