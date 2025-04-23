#Author : T.Jeffrin Santon
#Date : 01/03/2025
"""
#To Find Factorial
def _factorial(x):
    fact = 1
    while x==0:
        fact *= x
        x -= 1
    return fact
"""
#To Find The next derivative
def _derivative(points):
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
        cur_function = _derivative(cur_function)

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

