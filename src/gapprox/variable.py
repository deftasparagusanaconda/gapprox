class Variable:
	def __init__(self, name:str):
		self.name = name

	def __eq__(self, other):
		if not isinstance(other, Variable):
			return NotImplemented
		return self.value == other.value

	def __hash__(self):
		return hash(self.name)

	def __repr__(self):
		return f"<gapprox.Variable(value={self.name}) at {hex(id(self))}>"

def variables(*args):
	for arg in args:
		yield Variable(arg)
