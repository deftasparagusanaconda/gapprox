class Expression():
	'represents a mathematical expression. typically holds a string, but does not encode any meaning to its variables or constants'
	def __init__(self, value:str):
		self.value = value
	
	def __str__(self):
		return self.value

	def __repr__(self):
		return f"<gapprox.Expression(value={self.value}) at {hex(id(self))}>"
