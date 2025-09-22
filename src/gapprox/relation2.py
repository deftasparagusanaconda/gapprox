rom .mapping import Mapping
from typing import Callable, Iterable

class Relation:
	"""represents a relation. it can be represented as a directed bipartite graph, or as two dicts (two adjacency lists) or as a pair of callables that return a set. 

	technically, the relation can be completely captured unidirectionally but storing the relation bidirectionally allows O(1) access in both directions as opposed to O(1) in one direction and O(n) for the other if we were to store unidirectionally
	"""
	
	def __init__(
			self,
			domain: set  | Callable[..., bool],
			codomain: set  | Callable[..., bool],
			mapping: dict[any, set[any]] | Callable[..., bool] | Mapping):
		self.domain: set  | Callable[..., bool] = domain
		self.codomain: set  | Callable[..., bool] = codomain
		self.forward: dict[any, set[any]] | Callable[..., bool] | Mapping = mapping
		self.backward: dict[any, set[any]] | Callable[..., bool] | Mapping = mapping
	
	def __repr__(self) -> str:
		return f"<Relation at {hex(id(self))}: domain={self.domain!r}, codomain={self.codomain!r}, mapping={self.mapping!r}>"

	def __str__(self) -> str:
		output = f"Relation at {hex(id(self))}"
		output += f"\n    domain: {type(self.domain)}"
		if isinstance(self.domain, Iterable) and not callable(self.domain):	# because callables can be iterable, strangely
			output += f", len={len(self.domain)}"
		output += f"\n    codomain: {type(self.codomain)}"
		if isinstance(self.codomain, Iterable) and not callable(self.codomain):
			output += f", len={len(self.codomain)}"
		output += f"\n    mapping: {type(self.mapping)}"
		if isinstance(self.mapping, Iterable) and not callable(self.mapping):
			output += f", len={len(self.mapping)}"
		return output

	def domain_has(domain: any) -> bool:
		return domain in self.domain

	def codomain_has(codomain: any) -> bool:
		return codomain in self.codomain

	def mapping_has(domain: any, codomain: any) -> bool:
		return domain in mapping and mapping[domain] == codomain

	def get_domain(codomain: any) -> set[any]:
		if not self.codomain_has(codomain):
			raise ValueError(f"{codomain} not found in codomain")

		domain = self.domain[codomain]

		if not self.domain_has(codomain):
			raise ValueError(f"{domain} not found in domain")
	
		return domain

	def get_codomain(domain: any) -> set[any]:
		if not self.domain_has(domain):
			raise ValueError(f"{domain} not found in domain")

		codomain = self.codomain[domain]

		if not self.codomain_has(codomain):
			raise ValueError(f"{codomain} not found in codomain")
	
		return codomain

	__call__ = get_codomain
