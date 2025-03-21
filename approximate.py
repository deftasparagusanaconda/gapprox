import scipy.fft, sympy

#Author : T.Jeffrin Santon
#Date : 27/02/2025
def linear_approx(function , point_of_approx , delta):
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

def fft(inarr):
	output = "f(x) = \n"

	n = len(inarr)	# no. of points

	coefficients = scipy.fft.fft(inarr, norm="forward")
	
	realarr = numpy.real(coefficients)
	imagarr = -numpy.imag(coefficients)	# -ve because from both eulers formula and fft output, i**2 = -1

	for i in range(n):
		output += str(realarr[i])
		output += "*cos(2*pi*" + str(i) + '/' + str(n) + "*x) + "
		output += '\t'
		output += str(imagarr[i])
		output += "*sin(2*pi*" + str(i) + '/' + str(n) + "*x) + "
		output += '\n'

	# should return a string
	return output
	

#    dct_type: 1, 2, 3, 4 
#  input_type: "values", "params"
# output_type: "values", "params", "terms", "string", "matrix", "matrix_symbolic", "values_symbolic"
def dct(inarr, dct_type = 2, input_type = "values", output_type = ["values"]):
	if dct_type in [5,6,7,8]:
		raise ValueError("dct_type " + str(dct_type) + " is not yet implemented")
	elif dct_type not in [1,2,3,4]:
		raise ValueError("dct() got invalid dct_type")
	
	params = []
	if "params" == input_type:
		params = inarr
	elif "values" == input_type:
		params = scipy.fft.dct(inarr, type=dct_type, norm="forward")
	else:
		raise ValueError("dct() got invalid input_type")

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
		raise RuntimeError("dct() reached unexpected execution path")
	
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

#    dst_type: 1, 2, 3, 4
#  input_type: "values", "params"
# output_type: "values", "params", "terms", "string", "matrix", "matrix_symbolic", "values_symbolic"
def dst(inarr, dst_type = 2, input_type = "values", output_type = ["values"]):
	if dst_type in [5,6,7,8]:
		raise ValueError("dst_type " + str(dst_type) + " is not yet implemented")
	elif dst_type not in [1,2,3,4]:
		raise ValueError("dst() got invaolid dst_type")

	params = []
	if "params" == input_type:
		params = inarr
	elif "values" == input_type:
		params = scipy.fft.dst(inarr, type=dst_type, norm="forward")
	else:
		raise ValueError("dst() got invalid input_type")
	
	output = []

	if "params" in output_type:
		output.append(params)
	
	N = len(inarr)
	x = sympy.symbols("x")
	terms = []

	if 1 == dst_type:
		terms = (	2 * params[i] * sin(pi*(x+1)*(i+1)/(N+1)) for i in range(N))

	elif 2 == dst_type:
		terms = [	2 * params[i] * sin(pi*(i+1)*(2*x+1)/(2*N)) for i in range(N)]
		terms[-1] /= 2
	elif 3 == dst_type:
		terms = (	2 * params[i]) * sin(pi*(x+1)*(2*i+1)/(2*N)) for i in range(N))

	elif 4 == dst_type:
		terms = (	2 * params[i] * sin(pi*(2*x+1)*(2*i+1)/(4*N)) for  in range(N))

	else:
		raise RuntimeError("dst() reached unexpected execution path")

	if "terms" in output_type:
		output.append(terms)

	if "string" in output_type:
		output.append(	"f(x) = \n" + "\n+ ".join(str(term) for term in terms)	)

	# matrix[term][value] = term.subs(x,value)
	matrix_symbolic = [[term.subs(x,i) for i in range(N)] for term in terms]

	if "matrix_symbolic" in output_type:
		output.append(matrix_symbolic)
	
	if "matrix" in output_type:
		output.append(tuple(tuple(val.evalf() for val in term) for term in matrix_symbolic))

	values_symoblic = []
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
