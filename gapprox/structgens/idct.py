
def idct(params, idct_type=2, output_type="values"):
	"""
	inverse discrete cosine transform
	idct_type: 1, 2, 3, 4
	output_type: "values", "terms", "string", "matrix_symbolic", "matrix", "values_symbolic"
	"""
	import scipy.fft, sympy

	if idct_type in (5,6,7,8):
		raise ValueError(f"idct_type {idct_type} is not yet implemented")
	elif idct_type not in (1,2,3,4):
		raise ValueError("idct() got invalid idct_type")
	
	output = []

	if "values" in output_type:
		output.append(scipy.fft.idct(params, type=idct_type))

	N = len(params)
	x = sympy.symbols("x")

	if 1 == idct_type:
		terms = [2*params[i] * sympy.cos(sympy.pi*x/(N-1)*i) for i in range(N)]
		terms[0] /= 2
		terms[-1] /= 2
	elif 2 == idct_type:
		terms = [2*params[i] * sympy.cos(sympy.pi*(2*x+1)/(2*N)*i) for i in range(N)]
		terms[0] /= 2
	elif 3 == idct_type:
		terms = (2*params[i] * sympy.cos(sympy.pi*x*(2*i+1)/(2*N)) for i in range(N))
	elif 4 == idct_type:
		terms = (2*params[i] * sympy.cos(sympy.pi*(2*x+1)*(2*i+1)/(4*N)) for i in range(N))
	else:
		raise RuntimeError("idct() reached unexpected execution path")
	
	if "terms" in output_type:
		output.append(terms)
	
	if "string" in output_type:
		output.append(	"f(x) =\n  " + "\n+ ".join(str(term) for term in terms)	)
	
	matrix_symbolic = ((term.subs(x,i) for i in range(N)) for term in terms)
	
	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)
	if "matrix" in output_type:
		output.append(((val.evalf() for val in term) for term in matrix_symbolic))
	
	if "values_symbolic" in output_type:
		output.append(tuple(sum(term[i] for term in matrix_symbolic) for i in range(N)))
	
	if 1 == len(output):
		return output[0]
	else:
		return output

