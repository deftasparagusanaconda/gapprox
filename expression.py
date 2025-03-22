# fourier_series, cosine_series, sine_series, idft, idct, idst maintained by deftasparagusanaconda

"""
# y = a*x + b
def line(params, output_type = ["values"], force = False):
	if 2 != len(params) and False == force:
		return ValueError("line() got", len(params), "parameters")
	#elif True == force:
	
	output = []
	
	#if "values" in output_type:
	#	for i in range():
	
	
	if "string" in output_type:
		output.append(str(params[0]) + "*x + " + str(params[1]))
	
	return output

# y = a*x**2 + b*x + c
#def parabola(params, output_type = ["values"], force = False):
#	if 
"""
#Author : T.Jeffrin Santon
#Date : 27/02/2025
def linear_approx(function, point_of_approx , delta):
    #x-coordinates
    t = point_of_approx - delta
    z = point_of_approx + delta
    # Y-Coordinates
    x = t
    y1 = eval(function)
    x = z
    y2 = eval(function)
    #slope of the tangent calculation
    slope = (y2-y1)/(z - t)
    x = point_of_approx
    y = eval(function)
     #the output will be a stringi
    output = "y- " + str(y) + " = " + str(slope) +"(x - " + str(x) + ")";
    return output

#Author: T. Jeffrin Santon
#Date: 28/02/2025
def linear_d_approx(data_points , point_of_approx , position):
    #Slope calculation
    slope = (data_points[position + 1][1] - data_points[position - 1][1])/(data_points[position + 1][0] - data_points[position - 1][0])
    print(slope) #debugging
    output = "y - " + str(point_of_approx[1]) + " = "  + str(slope) + "(x - " + str(point_of_approx[0])+ ")"
    return output

#Author : T.Jeffrin Santon
#Date : 27.02.2025
def linear_Regression(points , no_of_points):
    summation_x ,summation_xy , summation_sqx ,summation_y = 0 , 0 , 0 , 0
    slope = 0.0
    y_intercept = 0.0
    for i in  range(no_of_points):
        summation_x += points[i][0]
        summation_y += points[i][1]
        summation_sqx += points[i][0]*points[i][0]
        summation_xy += points[i][0]*points[i][1]
    #slope calculation
    slope = ((no_of_points*summation_xy) - (summation_x*summation_y))/((no_of_points*summation_sqx) - (summation_x * summation_x))
    #Y-Intercept calculation
    y_intercept = (summation_y - (slope*summation_x))/no_of_points
    output = "y = " + str(slope) + "x" + " + " + str(y_intercept) 
    return output

#Author : T.Jeffrin Santon
#Date : 01/03/2025

#To Find Factorial
def factorial(x):
    fact = 1
    while x==0:
        fact *= x
        x -= 1
    return fact
#To Find The next derivative
def derivative(points):
    #Find the length
    points_len = len(points)

    #Slope array
    derivative_array = []

    for i in range(1 , points_len-1):
        slope = (points[i+1][1]-points[i-1][1])/(points[i+1][0]-points[i-1][0])
        print(slope)
        #slope at nearby position
        derivative_array.append([points[i][0] , slope])
    return derivative_array

#Kind of main
def taylor_series(points , point_of_approx ,no_of_terms):
    approx_function = "f(x) = "  
    approx_function += str(point_of_approx[1]) + "+"
    cur_function = points
    for i in range(1 , no_of_terms):
        cur_function = derivative(cur_function)

        for j in range(0 , len(cur_function)):
            if point_of_approx[0] == cur_function[j][0]:
                approx_function += str(cur_function[j][1])
                break
            if j == len(cur_function)-1:
                approx_function +=  "(x -" +str(point_of_approx[0]) + ")" + "^" + str(i)
                return approx_function 
        approx_function += "(x - " + str(point_of_approx[0]) + ")" + "^" +str(i)
        approx_function += "+"
    return approx_function

def fourier_series(params: list[complex], output_type="values"):
	"""
	output_type: "terms", "string", "matrix_symbolic", "matrix", "values_symbolic", "values"
	"""
	import scipy.fft, sympy, numpy
	
	output = []
	
	if "values" in output_type:
		output.append(scipy.fft.ifft(params, norm="forward"))
	
	x = sympy.symbols("x")
	N = len(params) # no of terms
	L = N

	if numpy.iscomplexobj(params):
		terms = tuple((params[i].real()*sympy.cos(i*sympy.pi*x/L) - params[i].imag()*sympy.sin(i*sympy.pi*x/L)) for i in range(N))
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

def cosine_series(params, output_type="values"):
	"""
	https://en.wikipedia.org/wiki/Fourier_sine_and_cosine_series
	output_type: "terms", "string", "matrix_symbolic", "matrix", "values_symbolic", "values"
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

import functools as _functools
idft = _functools.partial(fourier_series, L=None)

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

#print(fourier_series([5,4,3,2], output_type="matrix_symbolic"))
#print(sine_series([2,3,4,5]))

# to-do: implement output_types for idft 
