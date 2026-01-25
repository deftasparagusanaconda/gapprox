from inspect import Signature, BoundArguments, Parameter
import warnings	# for when arguments are given partially
import gapprox	# for gapprox.debug

def input_metadata(*args, **kwargs):
	"""a decorator to assign metadata to each parameter in a function. it is stored as a .input_metadata attribute to the function. the attribute is an instance of insect.BoundArguments.

	examples
	--------
	>>> @input_metadata('opposite', 'base', c = 'hypotenuse')
	>>> def triangle(a: float, /, b: int = 2, *args, c: float, **kwargs) -> tuple[float, float]:
	>>>     sum = a + b + c
	>>>     prod = a * b * c
	>>>     return sum, prod
	>>>
	>>> print(triangle.input_metadata)
	<BoundArguments (a='opposite', b='base', c='hypotenuse')>
	>>> print(triangle(3, 4, c = 5))
	(12, 60)

	as you can see, the metadata takes the same shape as is defined in the function inputs, and does not affect how the function works. it is simply just metadata lying around for you to decide what to use it for.
	"""

	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @input_metadata being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@input_metadata would return the decorator, not the function. use @input_metadata(...) instead')

	def decorator(function):
		signature: Signature = Signature.from_callable(function)
		function.input_metadata: BoundArguments = signature.bind_partial(*args, **kwargs)
		
		if gapprox.debug:
			# detect missing parameters
			missing = {parameter for parameter in signature.parameters if parameter not in function.input_metadata.arguments}
			if missing:
				warnings.warn(f"partial input_metadata given for {function.__name__}, missing: {missing}", stacklevel=2)
		
		return function
	return decorator

def input_metadata(*args, **kwargs):
	"""a decorator to assign metadata to each parameter in a function. it is stored as a .input_metadata attribute to the function. the attribute is an instance of insect.BoundArguments.

	examples
	--------
	>>> @input_metadata('opposite', 'base', c = 'hypotenuse')
	>>> def triangle(a: float, /, b: int = 2, *args, c: float, **kwargs) -> tuple[float, float]:
	>>>     sum = a + b + c
	>>>     prod = a * b * c
	>>>     return sum, prod
	>>>
	>>> print(triangle.input_metadata)
	<BoundArguments (a='opposite', b='base', c='hypotenuse')>
	>>> print(triangle(3, 4, c = 5))
	(12, 60)

	as you can see, the metadata takes the same shape as is defined in the function inputs, and does not affect how the function works. it is simply just metadata lying around for you to decide what to use it for.
	"""

	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @input_metadata being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@input_metadata would return the decorator, not the function. use @input_metadata(...) instead')

	def decorator(function):
		signature: Signature = Signature.from_callable(function)
		function.input_metadata: BoundArguments = signature.bind_partial(*args, **kwargs)
		
		if gapprox.debug:
			# detect missing parameters
			missing = {parameter for parameter in signature.parameters if parameter not in function.input_metadata.arguments}
			if missing:
				warnings.warn(f"partial input_metadata given for {function.__name__}, missing: {missing}", stacklevel=2)
		
		return function
	return decorator

def output_metadata(*args, **kwargs):
	"""a decorator to assign metadata to each parameter in a function. it is stored as a .output_metadata attribute to the function. the attribute is an instance of inspect.BoundArguments.
	
	the metadata is independent of the output arguments defined in the function, and does not affect how the function works. it is simply just metadata lying around for you to decide what to use it for.
	"""
	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @output_metadata being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@output_metadata would return the decorator, not the function. use @output_metadata(...) instead')

	def decorator(function):
		signature: Signature = Signature((Parameter('args', kind=Parameter.VAR_POSITIONAL), Parameter('kwargs', kind=Parameter.VAR_KEYWORD)))
		function.output_metadata: BoundArguments = signature.bind_partial(*args, **kwargs)
		return function

	return decorator

