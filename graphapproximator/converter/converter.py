def converter(input, output_type):
	"""detects input type and outputs chosen output_type
string -> parser -> function
function -> sampler -> points
points -> interpolator -> string"""

	import parser, sampler, interpolators
	interpolator = interpolators.linear

	if isinstance(input, str):	# string
		if output_type == "function":
			return parser(input)
		elif output_type == "points":
			return sampler(parser(input))
		else:
			raise ValueError

	elif callable(input):		# function
		if output_type == "points":
			return sampler(input)
		elif output_type == "string":
			return interpolator(sampler(input))
		else:	
			raise ValueError

	elif hasattr(input, "__iter__"):	# iterable/array
		if output_type == "string":
			return interpolator(input)
		elif output_type == "function":
			return parser(interpolator(input))
		else:	
			raise ValueError
	
	else:
		raise ValueError
	
