#from __future__ import annotations
from typing import Any as _Any, Sequence as _Sequence, Union as _Union, Callable as _Callable
from collections import OrderedDict as _OrderedDict

# marker object to denote a scalar value
Scalar = object()
# use 'if thing is Scalar:' to check whether a value is a Scalar or not.
# the following will not work:
# 'if isinstance(thing, Scalar):'
# 'if isinstance(thing, type(Scalar))'
# 'if type(thing) == Scalar'
# 'if type(thing) == type(Scalar)'
# the main thing to note is that its like checking against python's None/NoneType

# recursive typehints. pretty cool huh? :D
#NestedOrderedDict = _Union[_Any, _OrderedDict[_Any, 'NestedOrderedDict']]
#NestedDict = _Union[_Any, dict[_Any, 'NestedDict']]
NestedMixedDict = _Union[_Any, dict[_Any, 'NestedMixedDict'] | _OrderedDict[_Any, 'NestedMixedDict']]

class Shape:
	"""a class to denote the shape of some value. sometimes we want a tuple of coordinates to be treated as a single scalar value, instead of a vector of coordinates. this class solves that problem by allowing you to store metadata about it.

	each axis and each value is required to have a marker. it is most recommended to have a str marker.

	for convenience, the constructor accepts both dict and OrderedDict, because in python ≥3.7, dict preserves insertion order. but for semantic clarity, it is converted to OrderedDict anyway, since ordering is implied with dict, but explicit with OrderedDict.
	"""
	
	_ALLOW_EMPTY_SHAPE_DIMENSIONS: bool = False
	
	def __init__(self, tree: dict | _OrderedDict):
		# the data structure holding both the names and the values in nested OrderedDict
		self.tree: NestedOrderedDict = Shape._convert_to_nested_ordereddict(tree)

		# how many dimensions are described
		self.dimensions: int = Shape._get_nested_dict_depth(self.tree)
		
		# markers of each scalar value, laid out as a regular/ragged tensor of markers, dropping the axis markers
		#self.value_markers = Shape.	
		
		# how many scalar values are present in the shape
		self.value_count: int = Shape._count_leaves(self.tree)

		# whether each dimension has consistent length
		self.is_regular: bool = Shape._check_regularity(self.tree)
	
	@staticmethod
	def _convert_to_nested_ordereddict(thing: dict | _OrderedDict):
		if isinstance(thing, (dict, _OrderedDict)):
			return _OrderedDict((key, Shape._convert_to_nested_ordereddict(val)) for key, val in thing.items())	# recursion
		else:
			return thing	# termination
	
	@staticmethod
	def _get_nested_dict_depth(thing: dict | _OrderedDict, *, allow_empty_dimensions: bool = _ALLOW_EMPTY_SHAPE_DIMENSIONS) -> int:
		if not isinstance(thing, (dict, _OrderedDict)):
			return 0	# termination
		
		if len(thing) <= 0:
			if allow_empty_dimensions:
				return 1	# termination
			else:
				raise ValueError('degenerate dimension with no values found. empty dicts are not valid')
		
		return max(Shape._get_nested_dict_depth(value, allow_empty_dimensions = allow_empty_dimensions) for value in thing.values()) + 1	# recursion
	
	@staticmethod
	def _count_leaves(thing: dict | _OrderedDict) -> int:
		if not isinstance(thing, (dict, _OrderedDict)):
			return 1  # termination
		return sum(Shape._count_leaves(v) for v in thing.values())	# recursion

	# NOTE: this particular method was AI-generated and i havent verified it since.
	@staticmethod
	def _check_regularity(thing: dict | _OrderedDict) -> bool:
		"""Check if all branches have the same structure (regular tensor)."""
		if not isinstance(thing, (dict, _OrderedDict)):
			return True  # scalar leaf is trivially regular

		lengths = []
		
		for v in thing.values():
			if not isinstance(v, (dict, _OrderedDict)):
				lengths.append(1)
			else:
				lengths.append(len(v))

		# all same length at this level
		if len(set(lengths)) > 1:
			return False

		# recursively check children
		return all(Shape._check_regular(v) if isinstance(v, (dict, _OrderedDict)) else True for v in thing.values())
	
	def __repr__(self) -> str:
		dimensions_str = f"{self.dimensions} dimension{'s' if self.dimensions > 1 else ''}"
		value_count_str = f"{self.value_count} value{'s' if self.value_count > 1 else ''}"
		is_regular_str = 'regular' if self.is_regular else 'irregular'
		return f"<Shape at {hex(id(self))}: {dimensions_str}, {value_count_str}, {is_regular_str}>"

def output_shape(*args, **kwargs):
	"""a decorator that sets a .output_shape attribute on the function to denote information about the shape of the return value. the output_shape is an instance of the Shape class, constructed by parameters passed to this decorator.
	
	examples
	--------
	@output_shape('thing') 
		denotes just a scalar value named 'thing'. this is just a 0D vector
	
	@output_shape({'thing': Scalar})
		denotes a 1D vector of just one scalar value named 'thing'
	
	@output_shape({'mag': Scalar, 'arg': Scalar})
		denotes a 1D vector with two scalar values
	
	@output_shape({'space': {'length': Scalar, 'breadth': Scalar, 'height': Scalar}, 'time': Scalar})
		denotes a 2D vector 

	for more insight, see the Shape class. the arguments passed into output_shape are directly passed into the constructor of Shape. 
	
	returns
	-------
	a decorator that simply returns the attributed function
	
	explanation: 
		since a decorator cant take arguments, we instead make output_shape be a decorator that returns an argument-less decorator. that is one reason why you cant use '@output_shape' directly, as it returns a decorator, not the function
	
	notes
	-----
	- the recursive typehint Shape for the shape parameter is defined as:
		Shape = _Union[Scalar, _OrderedDict[str, 'Shape']]
	- the arguments passed into output_shape are directly passed into the constructor of Shape
	"""

	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @output_shape being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@output_shape would return the decorator, not the function. use @output_shape(...) instead')

	def decorator(function):	
		function.output_shape: Shape = Shape(*args, **kwargs)
		return function
	return decorator

'''
def attributes(**kwargs):
	"""a decorator that assigns its keyword arguments as attributes to a function"""

	def decorator(function):
		for key, value in kwargs.items():
			#function.key = value
			setattr(function, key, value)
		return function
	return decorator
'''

# ------------------------------------------------------------------------------
# huge rant i had while trying to figure out how to store return value information

# about .shape... 
# if shape = (1,), its a 1D vector of length 1
# if shape = (3,), its a 1D vector of length 3
# if shape = (2,2), its a 2D vector of length 2 and 2
# so dimensions = len(shape)
#
# furthermore, if shape = (,), its a 0D vector. this denotes a scalar.
# if dimensions = len(shape) = 0, it is a scalar
# furthermore, when theres no dimensions to denote a scalar, we can safely assume that the scalar will carry only one value.
# 
# we enforce that shape is ALWAYS a tuple, even if we want to denote a scalar. 
# so shape = 4 denoting a 1D vector of length 4 is disallowed
# and shape = None denoting a scalar is disallowed
# 
# to give names to each dimension and value of the shape, we could instead store an odict[str[...]] where ... can be either Any or odict[str[...]]
# thus shape could instead be:
# shape = 'thing' denoting a scalar value with the name 'thing'
# shape = ('thing') denoting a 1D vector of length 1. the first value in the 1st dimension is named 'thing'
# shape = ('mag', 'arg') denoting a 1D vector-valued function returning a 2-tuple of 'mag' and 'arg'
# shape = ({'space': ('length', 'breadth', 'height')}, 'time') denoting a 2D vector-valued function returning a 2-tuple. the first is the spatial dimensions, the second is the time dimension. inside the 'space' value, we have 'length', 'breadth', and 'height', in that specific order
# 
# so in the first case of an unnamed shape, len(shape) simply denotes the dimensionality.
# in the second case of a named shape, the nesting depth instead denotes the dimensionality.
# the scalar is not nested, so it has depth = 0, so, as we expect, it is a 0D vector which is a scalar
# the 1D vector is nested once within a tuple. so it is a 1D vector
# the 2D vector nests a dict within a tuple, so it is a 2D vector.
# 
# the problem with the named shape right now is that tuple and dict are both used, which makes shaping dimensions very hard. we should try to use one data structure, which will make shaping consistent. which one shall it be?
# 
# we shall have nested odicts for a namedshape. thus the previous examples come out to be:
# 
# shape = 'thing' for a scalar value with the name 'thing'	(0 nesting depth means 0D vector, which means a scalar)
# shape = {'thing': scalar} for a 1D vector value with one value named 'thing' which is a scalar. (1D because its nested once)
# shape = {'mag': scalar, 'arg': scalar} for a 1D vector value with two values.
# shape = {'space': {'length': scalar, 'breadth': scalar, 'height': scalar}, 'time': scalar} for a 2D vector
# 
# the "scalar" thing i used is a singleton object used to denote that a value is a scalar value, and will not be nested any further. essentially, it acts as a leaf node marker. it will have no semantic use or meaning or mechanism other than a marker
# the dimensionality of the vector is determined by the nesting depth of the odicts. 
# 
# a disadvantage is that we cant really have unnamed axes... say we want to give names to the space dimensions but we dont want to name the time dimension. how do we handle this case?
# 
# this may be a bolder move than you are usually used to from most other systems, but we DONT handle that case. we have a few bad solutions:
# solution 1: the system will have to learn to refer to an axis by one or the other. the system will have to handle edge cases everytime it wants to refer to an axis. this is VERY bad (i have experienced a laterally related 'handle edge case everytime you access something' problem with another system in the past (when i was separating gapprox's expression and DAG systems) and it is NOT elegant. it makes code utterly unreadable and unworkable. okay okay anyway moving on, sorry for the rant
# solution 2: the system will name things for the user, and auto-generate names for each unnamed axis or value. this is bad because we start baking in defaults into the system that the user has to know about. this makes the computer unpredictable. i want computers to be predictable. i dont want my computer to assume i want my file to be named unnamed.txt when i simply press Save. i want it to ask me a name. so i dont want this solution
# solution 3: we force the user to name every axis and value. this way the user is forced to be careful of how lazy they are in naming their dimensions. if they dont care about a name, they would give a name they dont care about. simple as that. the system will always be able to refer to a dimension by a name, even if its a bad one
# 
# so we choose solution 3. now a function may either have an unnamed shape or a named shape. either they give names to every axis and value, or they dont. we still have to choose between: force only unnamed shapes, force only named shapes, allow either
# why do i ask this? because the system will have to learn to work with both if we allow both, which slightly complicates the system. 
# 
# another disadvantage of an unnamed shape that i never mentioned is that it only denotes a regular tensor. simply stating the length of each axis assumes that it is regular. but if we arrange scalar objects into nested tuples, we can start denoting ragged tensors as well. this is more powerful. the unnamed shape already naturally supports ragged tensors.
# 
# so we actually have three shape notations: 
# 1. regular tensor: a tuple of ints, each denoting the length of an axis
# 2. ragged tensor: nested tuples of scalar objects
# 3. named tensor: nested odicts of scalar object leaves
# 
# the main gripe i have with this is that the system has to learn to deal with three kinds of shape notations. this is really bad. shall we choose two? with two, we still have casing based on shape notation. if we choose one canonical shape notation, we dont have to worry about any casing and the internal code for anything relying on .shape is cleaner.
# 
# if we were to choose two, i would choose ragged tensor and named tensor notations.
# if we were to choose one, i would choose named tensor notation.
# 
# here is the verdict: regular tensor notation cannot describe ragged tensor or named tensor. ragged tensor cannot describe named tensor. but a named tensor can describe both. clearly, even though it is the most complicated and verbose, it carries the most information. this shall be the canonical description of shape.
#
# final verdict: the shape of something will be defined with nested odict[str, ...] where ... can be either odict[str, ...] or scalar. each axis and each value will be assigned a name BY THE USER (the system will never name any of them for the user with default names like axis1, value1, etc.)
