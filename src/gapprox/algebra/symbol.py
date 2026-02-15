# instead of storing a str in the expression graph, we store Symbol. this way, we remember the meaning through an ID that a proper object encodes, instead of a str. furthermore, this allows us to encode metadata about something in the thing itself, instead of into the context dict.
# thus instead of context: dict[str, Symbol], we have context: dict[Symbol, value]
# thus a symbol should be able to encode all the information we want right in there. 
# the context simply provides a pragmatic value to the meaning we have defined in Symbol

from typing import Any

class Symbol:
	'a Symbol encodes meaning, like encoding the meaning of pi, instead of just the value'
	
	def __init__(self, name: str):
		# we INTENTIONALLY leave out value, because, mathematically, when we mean pi, we dont mean 'oh! pi! you mean python's math.pi!'. we mean 'ah, pi. the transcendental number, not the pragmatic float value we use in computers'
		self.name: str = name

	def __repr__(self) -> str:
		return f"<Symbol at {hex(id(self))}: name = {self.name}>"

	#def __add__(self, value, /):
	

class FunctionSymbol(Symbol):
	def __init__(self, name: str, arity: int):
		super().__init__(name)
		self.arity = arity

class ConstantSymbol(Symbol):
	...

