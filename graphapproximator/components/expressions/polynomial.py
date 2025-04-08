# f(x) = a + b*x + c*x^2 + d*x^3 + e*x^4 + ...
def polynomial(coefficients, x_start=None, x_stop=None, x_step=None, number_of_points:int=None, include_endpoint:bool=False, output_type:str|list[str]="values"):
	"""f(x) = a + b*x + c*x^2 + d*x^3 + e*x^4 + ...
polynomial(coefficients, x_start=None, x_stop=None, x_step=None, number_of_points=None, include_endpoint=False, output_type="values"):
	
	polynomial(coefficients, number_of_points=None)
	polynomial(coefficients, x_start=None, x_stop=None, x_step=None)
	polynomial(coefficients, x_start=None, x_stop=None, number_of_points=None)"""

	output = {}

	if "values" in output_type:
		values = []
		
		# only number of points is given
		if x_start is None and x_stop is None and x_step is None and number_of_points is not None:
			for x in range(number_of_points):
				values.append(sum(coefficient * x**index for index,coefficient in enumerate(coefficients)))

		# start, stop, step are given
		elif x_start is not None and x_stop is not None and x_step is not None and number_of_points is None:
			if include_endpoint:
				x_stop += x_step

			from numpy import arange
			for x in arange(x_start, x_stop, x_step):
				values.append(sum(coefficient * x**index for index,coefficient in enumerate(coefficients)))

		# start, stop, num are given
		elif x_start is not None and x_stop is not None and x_step is None and number_of_points is not None:
			from numpy import linspace
			for x in linspace(x_start, x_stop, num=number_of_points, endpoint=include_endpoint):
				values.append(sum(coefficient * x**index for index,coefficient in enumerate(coefficients)))

		else:
			raise ValueError(f"incorrect arguments: polynomial({coefficients}, x_start={x_start}, x_stop={x_stop}, x_step={x_step}, number_of_points={number_of_points}, include_endpoint={include_endpoint}, output_type={output_type}\n see print(polynomial.__doc__)")

		output["values"] = values

	if "string" in output_type:
		outstr = f"f(x) =\n  {coefficients[0]} * x**0"
		for index, coefficient in enumerate(coefficients[1:], start=1):
			outstr += f"\n+ {coefficient} * x**{index}"
		output["string"] = outstr
	
	if "symbolic" in output_type:
		from sympy import symbols
		x = symbols("x")
		expr = coefficients[0]
		for index, coefficient in enumerate(coefficients[1:], start=1):
			expr += coefficient * x**index
		output["symbolic"] = expr

	if len(output) == 1:
		return next(iter(output.values()))
	else:
		return output
