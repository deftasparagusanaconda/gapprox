# dft, dct, dst maintained by deftasparagusanaconda

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

def dft(values: list[complex]) -> list[complex]:
	"""discrete fourier transform"""

	import scipy.fft
	
	return scipy.fft.fft(values, norm="forward")
	
def dct(values, dct_type = 2):
	"""discrete cosine transform
	dct_type: 1, 2, 3, 4"""

	import scipy.fft
	
	if dct_type in [5,6,7,8]:
		raise ValueError(f"dct_type {dct_type} is not yet implemented")
	elif dct_type not in [1,2,3,4]:
		raise ValueError("dct() got invalid dct_type")
	
	return scipy.fft.dct(values, type=dct_type, norm="forward")

def dst(values, dst_type = 2):
	"""discrete sine transform
	dst_type: 1, 2, 3, 4"""

	import scipy.fft

	if dst_type in [5,6,7,8]:
		raise ValueError(f"dst_type {dst_type} is not yet implemented")
	elif dst_type not in [1,2,3,4]:
		raise ValueError("dst() got invalid dst_type")
	
	return scipy.fft.dst(values, type=dst_type, norm="forward")


# to-do: implement output_type=values_symbolic for dft(), dct(), dst()
