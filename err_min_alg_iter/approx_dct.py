import scipy.fft, sympy

#    dct_type: 1, 2, 3, 4 
#  input_type: "values", "params"
# output_type: "values", "params", "terms", "string", "matrix", "matrix_symbolic", "values_symbolic"
def approx_dct(inarr, dct_type = 2, input_type = "values", output_type = ["values"]):
	if dct_type in [5,6,7,8]:
		raise ValueError("dct_type " + str(dct_type) + " is not yet implemented")
	elif dct_type not in [1,2,3,4]:
		raise ValueError("approx_dct() got invalid dct_type")
	
	params = []
	if "params" == input_type:
		params = inarr
	elif "values" == input_type:
		params = scipy.fft.dct(inarr, type=dct_type, norm="forward")
	else:
		raise ValueError("approx_dct() got invalid input_type")

	output = []

	if "params" in output_type:
		output.append(params)

	N = len(inarr)
	x = sympy.symbols("x")
	terms = []

	if 1 == dct_type:
		terms = [2 * params[ i] * sympy.cos(sympy.pi*x/(N-1)*i) for i in range(N)]
		terms[0]  /= 2
		terms[-1] /= 2
	
	elif 2 == dct_type:
		terms = [2 * params[ i] * sympy.cos(sympy.pi*(2*x+1)/(2*N)*i) for i in range(N)]
		terms[0]  /= 2
	
	elif 3 == dct_type:
		terms = [2 * params[i] * sympy.cos(sympy.pi*x*(2*i+1)/(2*N)) for i in range(N)]
	
	elif 4 == dct_type:
		terms = [2 * params[i] * sympy.cos(sympy.pi*(2*x+1)*(2*i+1)/(4*N)) for i in range(N)]
	
	else:
		raise RuntimeError("approx_dct() reached unexpected execution path")
	
	if "terms" in output_type:
		output.append(terms)
	
	if "string" in output_type:
		output.append(	"f(x) =\n  " + "\n+ ".join(str(term) for term in terms)	)
	
	# matrix[term][value] = term.subs(x,value)
	matrix_symbolic = [[term.subs(x,i) for i in range(N)] for term in terms]
	
	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)
	
	if "matrix" in output_type:
		output.append(tuple(tuple(val.evalf() for val in term) for term in matrix_symbolic))
	
	values_symbolic = []
	for i in range(N):
		val = 0
		for term in matrix_symbolic:
			val += term[i]
		values_symbolic.append(val)
	
	if "values_symbolic" in output_type:
		output.append(values_symbolic)
	
	if "values" in output_type:
		output.append(tuple(val.evalf() for val in values_symbolic))
	
	return output
