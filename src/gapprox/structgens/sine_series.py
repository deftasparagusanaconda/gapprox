def sine_series(params, output_type="values"):
	"""
	https://en.wikipedia.org/wiki/Fourier_sine_and_cosine_series
	output_type: "terms", "string", "matrix_symbolic", "matrix", "values_symbolic", "values"
	"""
	import sympy
	
	output = []
	N = len(params)
	x = sympy.symbols("x")
	terms = (params[i] * sympy.sin(i*sympy.pi*x/(N+1)) for i in range(1,N+1))

	if "terms" in output_type:
		output.append(terms)
	
	if "string" in output_type:
		output.append(	"f(x) =\n  " + "\n+ ".join(str(term) for term in terms)	)
	
	matrix_symbolic = tuple((term.subs(x,i) for i in range(N)) for term in terms)
	
	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)	
	if "matrix" in output_type:
		output.append(((value.evalf() for value in term) for term in matrix_symbolic))

	values_symbolic = tuple(sum(term[i] for term in matrix_symbolic) for i in range(N))

	if "values_symbolic" in output_type:
		output.append(values_symbolic)
	if "values" in output_type:
		output.append(tuple(value.evalf() for value in values_symbolic))

	if 1 == len(output):
		return output[0]
	else:
		return output


