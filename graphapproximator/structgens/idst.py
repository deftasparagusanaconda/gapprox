def idst(params, idst_type = 2, output_type="values"):
	"""
	inverse discrete sine transform
	output_type: "values", "terms", "string", "matrix_symbolic", "matrix", "values_symbolic"
	"""
	import scipy.fft, sympy

	if idst_type in (5,6,7,8):
		raise ValueError(f"idst_type {idst_type} is not yet implemented")
	elif idst_type not in (1,2,3,4):
		raise ValueError("idst() got invalid idst_type")
	
	output = []

	if "values" in output_type:
		output.append((scipy.fft.idst(params, type=idst_type)))

	N = len(params)
	x = sympy.symbols("x")
	terms = []

	if 1 == idst_type:
		terms = (2*params[i] * sympy.sin(sympy.pi*(x+1)*(i+1)/(N+1)) for i in range(N))
	elif 2 == idst_type:
		terms = [2*params[i] * sympy.sin(sympy.pi*(i+1)*(2*x+1)/(2*N)) for i in range(N)]
		terms[-1] /= 2
	elif 3 == idst_type:
		terms = (2*params[i] * sympy.sin(sympy.pi*(x+1)*(2*i+1)/(2*N)) for i in range(N))
	elif 4 == idst_type:
		terms = (2*params[i] * sympy.sin(sympy.pi*(2*x+1)*(2*i+1)/(4*N)) for i in range(N))
	else:
		raise RuntimeError("idst() reached unexpected execution path")

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
		output.append((sum(term[i] for term in matrix_symbolic) for i in range(N)))
	
	if 1 == len(output):
		return output[0]
	else:
		return output

