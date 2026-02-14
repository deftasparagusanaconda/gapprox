from .relation import Relation
from collections.abc import Container, Sequence
from typing import Any, Callable

class Function(Relation):
	"""represents a mathematical function – either a partial or a total one. it is a right-unique binary relation from one domain to another, and is also left-total in the case of a non-partial "total" function. it stores the domains flatly as .domain and .codomain. unlike a Relation, it stores the 2-tuples as a dict or a callable, which is its indicator function of the set of 2-tuples. it also allows Mappings to assist in the lookup of domain or codomain
	
	a Function such as f(x, y) = x + y is just a function that takes a set of tuples as domain, instead of two domain sets. thus with conventional notation, functions are inherently positional with their arguments. it remembers this by storing a 
	"""

	def __init__(
			self,
			domain  : Container[Any],
			codomain: Container[Any],
			mapping : Callable[[Any], Any],
			) -> None:
		class tuples:
			def __contains__(tuple) -> bool:
				return mapping(tuple[0]) == tuple[1]
		
		self.mapping: Mapping[Any, Any] = mapping
		self.domains = domain, codomain
	
	# you might ask "we subclass Relation, but it doesnt even call the constructor". thats because python wasnt capable enough to communicate what i meant by a Relation. all it has to do is allow __contains__ and store domains. it doesnt actually have to let the tuples be iterable or such. and so we achieved exactly that anyway. Function has a relates(), and the Relation superclass links __contains__() to relates()
	
	def relates(self, tuple: Sequence[Any, Any]) -> bool:
		return self.mapping(tuple[0]) == tuple[1]

	# Relation defines __contains__ = relates
		
	def get_codomain(self, input: Any, check_domains: bool = True) -> Any:
		'also known as the image'
		if check_domains and input not in self.domains[0]:
			raise ValueError(f'{input} is not in {self.domains[0]}')

		output = self.mapping(input)

		if check_domains and output not in self.domains[1]:
			raise ValueError(f'{input} is not in {self.domains[0]}')

		return output

	__call__ = get_codomain

	def __repr__(self) -> str:
		return f"<Function at {hex(id(self))}: domains = {self.domains!r}, mapping = {self.mapping!r}>"

	def __str__(self) -> str:
		output = f"Function at {hex(id(self))}:"
		output += f"\n    domain: {type(self.domain)}"
		if isinstance(self.domain, Iterable) and not callable(self.domain):	# because callables can be iterable, strangely
			output += f", len={len(self.domain)}"
		output += f"\n    codomain: {type(self.codomain)}"
		if isinstance(self.codomain, Iterable) and not callable(self.codomain):
			output += f", len={len(self.codomain)}"
		output += f"\n    forward_mapping: {type(self.forward_mapping)}"
		if isinstance(self.forward_mapping, Iterable) and not callable(self.forward_mapping):
			output += f", len={len(self.forward_mapping)}"
		output += f"\n    reverse_mapping: {type(self.reverse_mapping)}"
		if isinstance(self.reverse_mapping, Iterable) and not callable(self.reverse_mapping):
			output += f", len={len(self.reverse_mapping)}"
		return output

		"""
		if gapprox.debug:
			if not isinstance(domain, Domain):
				raise ValueError("domain must be an instance of Domain")
			if not isinstance(codomain, Domain):
				raise ValueError("codomain must be an instance of Domain")
			if forward_mapping is not None and not isinstance(forward_mapping, Mapping):
				raise ValueError("forward_mapping must be an instance of Mapping")
			if tuples is not None and not isinstance(tuples, Domain):
				raise ValueError("tuples must be an instance of Domain")
			if reverse_mapping is not None and not isinstance(reverse_mapping, Mapping):
				raise ValueError("reverse_mapping must be an instance of Mapping")

			if any(codomain != forward_mapping(domain) for domain, codomain in tuples):
				raise ValueError("tuples and forward_mapping do not match")
			if any(domain != reverse_mapping(codomain) for domain, codomain in tuples):
				raise ValueError("tuples and reverse_mapping do not match")
			elif forward_mapping is not None and reverse_mapping is not None:
				if callable(forward_mapping) and callable(reverse_mapping):
					raise NotImplementedError
				elif callable(forward_mapping) and not callable(reverse_mapping):
					raise NotImplementedError
				elif not callable(forward_mapping) and callable(reverse_mapping):
					raise NotImplementedError
				elif not callable(forward_mapping) and not callable(reverse_mapping):
					if any(reverse_mapping != domain for domain, codomain in forward_mapping.items()):
						raise ValueError("forward_mapping and reverse_mapping do not match")
					if any(reverse_mapping != domain for domain, codomain in reverse_mapping.items()):
						raise ValueError("forward_mapping and reverse_mapping do not match")
				else:
					raise RuntimeError("impossible branch")
		"""
		
