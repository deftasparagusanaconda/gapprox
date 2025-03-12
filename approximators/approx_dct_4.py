from scipy.fft import dct
from sympy import symbols, cos, pi

# return types are "params", "terms", "string", "matrix", "values"
def approx_dct_4(inarr, return_type = "values"):
	params = dct(inarr, type=4, norm="forward")
	
	if "params" == return_type:
		return params
	
	N = len(inarr)
	x = symbols("x")
	terms = [2 * params[i] * cos(pi*(2*x+1)*(2*i+1)/(4*N)) for i in range(N)]
	
	if "terms" == return_type:
		return terms
	
	elif "string" == return_type:
		return "f(x) =\n  " + "\n+ ".join(str(term) for term in terms)

	# matrix[term][value] = term.subs(x,value)
	matrix = [[term.subs(x,i) for i in range(N)] for term in terms]
	
	if "matrix" == return_type:
		return matrix
	
	values = []
	for i in range(N):
		value = 0
		for term in matrix:
			value += term[i]
		values.append(value)
	
	if "values" == return_type:
		return values

	else:
		raise ValueError("approx_dct_4() got invalid return_type")
	
	raise RuntimeError("approx_dct_4() reached unexpected execution path")
