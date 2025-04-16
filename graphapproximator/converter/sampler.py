def sampler(function, mode:list|int|tuple, include_endpoint:bool=True):
	"""sample a function at discrete x values
	
sampler(function, mode, include_endpoint=False):
	
the following formats are supported:
sampler(function, [4, 3, 5, 1, ...])
sampler(function, number_of_points)	(assumes x = 0, 1, 2, ...)
sampler(function, (x_start, x_stop, number_of_points:int))
sampler(function, (x_start, x_stop, x_step:float))
"""	
	if isinstance(mode, list):
		x_array = mode

	elif isinstance(mode, int):
		x_array = list(range(mode))

	elif isinstance(mode, tuple):
		if len(mode) != 3:
			raise ValueError("correct usage is sampler((start, stop, step) or sampler(start, stop, num)")

		a, b, c = mode	# sampler(someexpression, (a,b,c))

		if isinstance(c, int):
			from numpy import linspace
			x_array = list(linspace(a,b,c, endpoint=include_endpoint))

		else:
			from numpy import arange
			x_array = list(arange(a, (b+c) if include_endpoint else b, c))
	
	else:
		raise ValueError(f"incorrect arguments. see print(sampler.__doc__)")
	
	return x_array, list(function(x) for x in x_array)
