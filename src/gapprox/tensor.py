class Tensor:
	"""a class to represent a scalar, vector, matrix, tensor, or the absence thereof

	ATTRIBUTES
	----------

	data:	any
		the actual data of the mutable tensor

	shape:	tuple[int]
		can be None, (), (a,), (a, b), (a, b, c), …

		len(shape) represents the dimensionality of the tensor
		if len(shape) == 0, it is a scalar
		if len(shape) == 1, it is a vector
		if len(shape) == 2, it is a matrix
		if len(shape) >2, it is a tensor
		if shape is None, it represents nullary, or "no tensor" or "no elements"


	
	"""
	def __init__(self, shape:tuple[int]):
		self.data = None
		self.shape:tuple[int] = shape
