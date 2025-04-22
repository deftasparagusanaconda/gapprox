def fourier_series(a_terms:list, b_terms:list=None, L=None):
	"""fourier_series(real, imag, L=None) returns fourier series
https://en.wikipedia.org/wiki/Fourier_series"""
	#if "values" in output_type:
	#	output.append(scipy.fft.ifft(params, norm="forward"))

	L = len(a_terms) if L is None else L
	
	if b_terms is None:
		terms = (f"{a_terms[n]}*cos({n}*pi*x/{L}) - 0*sin({n}*pi*x/{L})" for n in range(L))
	else:
		terms = (f"{a_terms[n]}*cos({n}*pi*x/{L}) - {b_terms[n]}*sin({n}*pi*x/{L})" for n in range(L))
	
	return " + ".join(str(term) for term in terms)

# add support for more complex inputs

"""
def fourier_series(params: list[complex], output_type="values"):

	output_type: "terms", "string", "matrix_symbolic", "matrix", "values_symbolic", "values"
	
	import scipy.fft, sympy, numpy
	
	output = []
	
	if "values" in output_type:
		output.append(scipy.fft.ifft(params, norm="forward"))
	
	x = sympy.symbols("x")
	N = len(params) # no of terms
	L = N

	if numpy.iscomplexobj(params):
		terms = tuple((params[i].real*sympy.cos(i*sympy.pi*x/L) - params[i].imag*sympy.sin(i*sympy.pi*x/L)) for i in range(N))
	else:
		terms = tuple((params[i]*sympy.cos(i*sympy.pi*x/L) for i in range(N)))

	if "terms" in output_type:
		output.append(terms)

	if "string" in output_type:
		output.append(	"f(x) =\n  " + "\n+ ".join(str(term) for term in terms)	)

	matrix_symbolic = tuple(tuple(term.subs(x,i) for i in range(N)) for term in terms)
	
	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)
	if "matrix" in output_type:
		output.append(tuple(tuple(val.evalf() for val in term) for term in matrix_symbolic))
	
	if "values_symbolic" in output_type:
		output.append((sum(term[i] for term in matrix_symbolic) for i in range(N)))
	
	if 1 == len(output):
		return output[0]
	else:
		return output
"""
