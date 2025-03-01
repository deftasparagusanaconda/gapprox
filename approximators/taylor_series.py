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

print(taylor_series([(-2.51, -1.84), 
(9.01, 20.43),
(4.64, 12.46),
(1.97, 2.97),
(-6.88, -11.20),
(-6.88, -10.05),
(-8.84, -11.72),
(7.32, 16.61),
(2.02, 5.43),
(4.16, 10.32),
(-9.59, -14.35),
(9.40, 22.45),
(6.65, 15.24),
(-5.75, -7.48),
(-6.36, -9.53),
(-6.33, -7.73),
(-3.92, -6.23),
(0.50, 3.33),
(-1.36, -0.51),
(-4.18, -8.28),
(2.24, 8.07),
(-7.21, -10.90),
(-4.16, -5.30),
(-2.67, -2.81),
(-0.88, -1.59),
(5.70, 13.57),
(-6.01, -9.70),
(0.28, 1.96),
(1.85, 6.37),
(-9.07, -14.33),
(2.15, 11.07),
(-6.59, -9.83),
(-8.70, -13.88),
(8.98, 20.81),
(9.31, 17.79),
(6.17, 15.28),
(-3.91, -4.69),
(-8.05, -8.17),
(3.68, 9.98),
(-1.20, 1.21),
(-7.56, -12.19),
(-0.10, 0.47),
(-9.31, -13.34),
(8.19, 20.88),
(-4.82, -5.07),
(3.25, 7.68),
(-3.77, -1.73),
(0.40, 0.99),
(0.93, 6.04),
(-6.30, -5.22)
] ,(0.5 , 3.33) , 10000))     
