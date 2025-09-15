class Constant:
	def __init__(self, name:str, value:int|float):
		self.name = name
		self.value = value

	def __eq__(self, other):
		if not isinstance(other, Constant):
			return NotImplemented
		return self.value == other.value

	def __hash__(self):
		return hash((self.name, self.value))

	def __repr__(self):
		return f"<gapprox.Constant(name={self.name},value={self.value}) at {hex(id(self))}>"	

def constants(*args):
	for arg in args:
		yield Constant(arg)
