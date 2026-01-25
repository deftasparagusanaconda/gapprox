def input_metadata(*args, **kwargs):
	"""a decorator to assign input metadata to a function. the following attributes are given to the function:

	function.input_args: tuple[...] = args
	function.input_kwargs: dict[str, ...] = kwargs

	example
	-------
	>>> @input_metadata(2, thing = 'hi!')
	>>> def triangle(a: float, /, b: int = 2, *args, c: float, **kwargs) -> tuple[float, float]:
	>>>     sum = a + b + c
	>>>     prod = a * b * c
	>>>     return sum, prod
	>>>
	>>> print(triangle.input_args, triangle.input_kwargs)
	(2,) {'thing': 'hi!'}
	>>> print(triangle(1, 2, c = 3))
	(6, 6)

	as you can see, the metadata is independent of whatever the function is doing. it is just metadata that doesnt do anything until you do something with it. it is also not modified and is passed exactly as it was given in the decorator's arguments.

	raises
	------
	ValueError
		when it is used as '@input_metadata' instead of '@input_metadata(...)'

	notes
	-----
	the signature of the arguments given to the input_metadata decorator need not match the signature of the function.
	"""


	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @input_metadata being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@input_metadata would return the decorator, not the function. use @input_metadata(...) instead')
	
	def decorator(function):
		function.input_args: tuple[...] = args
		function.input_kwargs: dict[str, ...] = kwargs

		return function

	return decorator

def output_metadata(*args, **kwargs):
	"""a decorator to assign output metadata to a function. the following attributes are given to the function:

	function.output_args: tuple[...] = args
	function.output_kwargs: dict[str, ...] = kwargs
	
	example
	-------
	>>> @output_metadata(2, thing = 'hi!')
	>>> def triangle(a: float, /, b: int = 2, *args, c: float, **kwargs) -> tuple[float, float]:
	>>>     sum = a + b + c
	>>>     prod = a * b * c
	>>>     return sum, prod
	>>>
	>>> print(triangle.output_args, triangle.output_kwargs)
	(2,) {'thing': 'hi!'}
	>>> print(triangle(1, 2, c = 3))
	(6, 6)

	raises
	------
	ValueError
		when it is used as '@output_metadata' instead of '@output_metadata(...)'

	as you can see, the metadata is independent of whatever the function is doing. it is just metadata that doesnt do anything until you do something with it. it is also not modified and is passed exactly as it was given in the decorator's arguments.
	"""
	# if the decorator is used without parentheses, the first argument is itself a function
	# we use that fact to disallow @output_metadata being used directly
	if len(args) == 1 and callable(args[0]):
		raise ValueError('@output_metadata would return the decorator, not the function. use @output_metadata(...) instead')

	def decorator(function):
		function.output_args: tuple[...] = args
		function.output_kwargs: dict[str, ...] = kwargs

		return function

	return decorator

