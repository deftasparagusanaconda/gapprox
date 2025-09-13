from .misc.count import count
import gapprox

class NodeVisitor:
	"""inspired by python's ast.NodeVisitor. see https://docs.python.org/3/library/ast.html#ast.NodeVisitor

	this class is really just a stateful function that traverses through nodes in a DAG. the difference is that it will have different logic for different kinds of nodes. you make a subclass of it, and there you define visit_* methods, where * is your node's class name. say you have ParameterNode. then you would define something like MutateParameterVisitor.visit_ParameterNode

	like ast.NodeVisitor, it defines visit and generic_visit, and subclasses are supposed to define visit_* (* meaning YourClassName)
	unlike ast.NodeVisitor, it does not define visit_Constant, is not specific to a tree structure, and is not specific to ast nodes. it supports a directed acyclic graph data structure, and is generic to *any* kind of DAG node (i think)
	"""
	def visit(self):
		'the thing to call to start traversal. never start traversal by calling visit_SpecificNodeType(mynode). always start traversal using visit(mynode)'

	def generic_visit(self):
		'the fallback method to call when the corresponding visit_* for the node type is not found'
		if gapprox.debug:
			raise ValueError("corresponding visit_* method was not found")
		else:
			return

	def __repr__(self):
		name_str = self.__class__.__name__	# in case derived classes dont implement their own __repr__ which they probably wont
		id_str = hex(id(self))
		methods_str = ""	#    TODO: how to get number of visit_* methods defined?
		return f"<{name_str}: {id_str}>"

	def __str__(self):
		from collections.abc import Iterable

		# all names in the instance
		all_names = dir(self)

		# filter out attributes and methods
		attributes = [name for name in all_names if not callable(getattr(self, name)) and not name.startswith("__")]
		methods    = [name for name in all_names if callable(getattr(self, name)) and not name.startswith("__")]

		output = f"self.__class__.__name__ (ID={hex(id(self))})"
		output += f"\nattributes: {len(attributes)} defined"
		for name in attributes:
			value = getattr(self, name)
			if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
				output += f"\n    {name} = {type(value)}, count={count(value)}, length={len(value)}"
			else:
				output += f"\n    {name} = {value}"
		output += f"\nmethods   : {len(methods)} defined"
		for method in methods:
			output += f"\n    {method}()"
		return output

class NodeTransformer(NodeVisitor):
	"""inspired by python's ast.NodeTransformer. see https://docs.python.org/3/library/ast.html#ast.NodeTransformer

	this class is really just a stateful function that traverses through nodes in a DAG, and replaces them along the way using the return value of their respective visit_* methods. this class is closely related with gapprox.NodeVisitor

	like ast.NodeTransformer subclassing ast.NodeVisitor, it subclasses gapprox.NodeVisitor
	unlike ast.NodeTransformer
	"""
