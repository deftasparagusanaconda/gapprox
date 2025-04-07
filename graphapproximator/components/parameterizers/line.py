#Author : T.Jeffrin Santon
#Date : 27.02.2025
def least_squares(points , no_of_points):
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
