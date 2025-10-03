# TODO:
# somehow register OrderedExpression as a Callable
# thus replace callable(thing) with isinstance(thing, Callable) wherever possible
# also try to support subscriptable typehinting for OrderedExpression and other classes

from collections.abc import Callable, Iterable, Sequence
import gapprox
from .ast_to_multidag_visitor import AstToMultiDAGVisitor
from .expression import Expression, OrderedExpression

class Domain:
	'represents a mathematical domain, which is stored as either a set, or a Callable[any, bool] which is the indicator function of that set'
	
	def __init__(self, determiner: set[any] | Callable | OrderedExpression):#[any, bool]):
		if not hasattr(determiner, '__contains__') and not callable(determiner):
			raise TypeError(f"{determiner} must have a __contains__ method, or be a callable")
		self.determiner = determiner
	
	def has(self, thing: any) -> bool:
		if hasattr(self.determiner, '__contains__'):
			return thing in self.determiner
		elif callable(self.determiner):
			return self.determiner(thing)	
		else:
			raise AttributeError("unrecognized determiner")

	__contains__ = has

class Mapping:
	"""represents an mapping. mathematically, an mapping is an looser term than an function but here it is simply an wrapper for any of: an LUT, an function, an set. it is unidirectional. it encodes a mapping from somewhere to some other where but without encoding where it maps to or from.

	the indicator function of a set[tuple] cannot act as a mapping because we must know the mapping beforehand to verify it
	"""
	def __init__(self, mapper:
				  dict[any, any]
		        | OrderedExpression#[any, any]
			    | Callable
				| Iterable[tuple[any, any]]):
		if gapprox.debug and not isinstance(mapper, (dict, OrderedExpression, Callable, Iterable)):
			raise ValueError("invalid mapper type. see help(gapprox.Mapping) to see allowed types")
		self.mapper = mapper
	
	def maps_to(self, something: any) -> any: 
		if isinstance(self.mapper, dict):	# dict, or some other container of tuples
			return self.mapper[something]
		elif callable(self.mapper):
			return self.mapper(something)
		else:
			raise ValueError(f"unsuppored mapper {self.mapper!r} of type {type(self.mapper)}")
	
	__call__ = maps_to

class Relation:
	"""represents a mathematical relation. it stores a set of tuples in .tuples and also keeps track of a tuple of domains in .domains. it thus generalizes to an n-ary relation. it can also store tuples as a callable, which is the indicator function of the set"""

	def __init__(self, tuples: set[tuple] | OrderedExpression, domains):#[tuple, bool], domains: tuple[Domain]):
		raise NotImplementedError("not fully done yet")
		self.tuples: set[tuple] | Callable[tuple, bool] = tuples
		self.domains: tuple[Domain] = domains
	
	def has(stuff: tuple) -> bool:
		if gapprox.debug:
			for thing, domain in zip(stuff, self.domains):
				if thing not in domain:
					raise ValueError("{thing!r} in domain {domain!r} is not in {self.domains!r}")
			
		if callable(self.tuples):
			return self.tuples(stuff)
		elif hasattr(self.tuples, '__contains__'):
			return stuff in self.tuples
		else:
			raise ValueError("unrecognized tuples {self.tuples!r}")

	__contains__ = has

class Function(Relation):
	"""represents a mathematical function – either a partial or a total one. it is a right-unique binary relation from one domain to another, and is also left-total in the case of a non-partial "total" function. it stores the domains flatly as .domain and .codomain. unlike a Relation, it stores the 2-tuples as a dict or a callable, which is its indicator function of the set of 2-tuples. it also allows Mappings to assist in the lookup of domain or codomain
	
	a Function such as f(x, y) = x + y is just a function that takes a set of tuples as domain, instead of two domain sets. thus with conventional notation, functions are inherently positional with their arguments. it remembers this by storing a """
	def __init__(
			self,
			domain         : Domain,#[any],
			codomain       : Domain,#[any],
			forward_mapping: Mapping=None,#[any, any] = None,
			tuples         : Domain=None,#[tuple[any, any]] = None,
			reverse_mapping: Mapping=None):#[any, set[any]] = None):
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
		self.domain         : Domain[any]             = domain
		self.codomain       : Domain[any]             = codomain
		self.forward_mapping: Mapping[any, any]       = forward_mapping
		self.tuples         : Domain[tuple[any, any]] = tuples
		self.reverse_mapping: Mapping[any, any]       = reverse_mapping

		if isinstance(self.forward_mapping, str):
			new_expr = Expression(self.forward_mapping)
			new_lambda = OrderedExpression(new_expr)
			self.forward_mapping: Mapping = Mapping(new_lambda)
		
	@property
	def is_partial(self) -> bool:
		'whether the Function is a partial function or a left-total function'
		return not any(thing in domain for thing in tuples)
	
	@property
	def active_domain(self) -> bool:
		'for a non-partial function, this is just the domain'
		raise NotImplementedError
	
	@property
	def active_codomain(self) -> bool:
		'also known as the range of a function'
		raise NotImplementedError
	
	def maps(domain: any, codomain: any) -> bool:
		'check whether the function maps some domain to some codomain'
		if gapprox.debug:
			if domain not in self.domain:
				raise ValueError(f"{domain} not defined in {self.domain}")
			if codomain not in self.codomain:
				raise ValueError(f"{codomain} not defined in {self.codomain}")
		
		if self.tuples is not None:
			return (domain, codomain) in self.tuples
		elif self.forward_mapping is not None:
			if callable(self.forward_mapping):
				return self.forward_mapping(domain) == codomain
			else:
				return self.forward_mapping[domain] == codomain
		elif self.reverse_mapping is not None:
			if callable(self.reverse_mapping):
				return self.reverse_mapping(codomain) == domain
			else:
				return self.reverse_mapping[codomain] == domain
		else:
			raise RuntimeError("critical error! unexpected branch. self.tuples, self.forward_mapping, and self.reverse_mapping were all None. constructor shouldnt have allowed that... maybe you changed attributes later on?")

	def get_codomain(self, domain: any) -> any:
		'also known as the image'
		if gapprox.debug and domain not in self.domain:
			raise ValueError(f"{domain} not defined in {self.domain}")

		if self.forward_mapping is None:
			raise ValueError(f"no forward_mapping given to get codomain")
		
		codomain = self.forward_mapping(domain)

		if gapprox.debug and codomain not in self.codomain:
			raise ValueError(f"{codomain} not defined in {self.codomain}")

		return codomain

	def get_domain(self, codomain: any) -> set[any]:
		'also known as the pre-image'
		if gapprox.debug and codomain not in self.codomain:
			raise ValueError(f"{codomain} not defined in {self.codomain}")

		if self.reverse_mapping is None:
			raise ValueError(f"no reverse_mapping given to get domain")
		
		domain = self.reverse_mapping(codomain)

		if gapprox.debug and domain not in self.domain:
			raise ValueError(f"{domain} not defined in {self.domain}")

		return domain

	__call__ = get_codomain

	def __repr__(self) -> str:
		return f"<Function at {hex(id(self))}: domain={self.domain!r}, codomain={self.codomain!r}, forward_mapping={self.forward_mapping!r}, tuples={self.tuples!r}, reverse_mapping={self.reverse_mapping!r}>"

	def __str__(self) -> str:
		output = f"Function at {hex(id(self))}"
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
the hierarchy is:
Node, Edge
Dag
Expression
OrderedExpression
Domain
Mapping
Relation
Function
"""
