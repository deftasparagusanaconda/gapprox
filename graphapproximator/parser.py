def parser(input:str):
	"""parse a string with x as independent variable
returns a callable function"""
	if "sin" in input:
		from math import sin
	if "cos" in input:
		from math import cos

	def function(x):
		return eval(input, {"x":x, "sin":math.sin, "cos":math.cos})

	return function
