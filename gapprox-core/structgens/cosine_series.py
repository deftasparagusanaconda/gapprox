def cosine_series(params, L=None):
	"""return string of cosine series
https://en.wikipedia.org/wiki/Fourier_sine_and_cosine_series"""
	
	if L is None:
		L = len(params)
	
	params[0] /= 2

	return " + ".join(f"{param}*cos({n}*pi*x/{L})" for n, param in enumerate(params))	

"""
	import sympy

	output = []
	N = len(params)
	x = sympy.symbols("x")
	terms = (params[i] * sympy.cos(i*sympy.pi*x/N) for i in range(N))

	if "terms" in output_type:
		output.append(terms)

	if "string" in output_type:
		output.append(	"f(x) =\n  " + "\n+ ".join(str(term) for term in terms)	)

	matrix_symbolic = tuple(tuple(term.subs(x,i) for i in range(N)) for term in terms)

	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)
	if "matrix" in output_type:
		output.append(((value.evalf() for value in term) for term in matrix_symbolic))

	values_symbolic = (sum(term[i] for term in matrix_symbolic) for i in range(N))

	if "values_symbolic" in output_type:
		output.append(values_symbolic)
	if "values" in output_type:
		output.append(tuple(value.evalf() for value in values_symbolic))

	if 1 == len(output):
		return output[0]
	else:
		return output
"""
