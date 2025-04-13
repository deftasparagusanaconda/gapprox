def parser(input:str):
	"""parse a string with x as independent variable
returns a callable function"""

	def function(x):
		return eval(input, {"x":x})

	return function
