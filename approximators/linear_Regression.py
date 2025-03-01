
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
points_array = [
    [-2.51, -1.84], [9.01, 20.43], [4.64, 12.46], [1.97, 2.97], [-6.88, -11.20],
  [-6.88, -10.05], [-8.84, -11.72], [7.32, 16.61], [2.02, 5.43], [4.16, 10.32],
  [-9.59, -14.35], [9.40, 22.45], [6.65, 15.24], [-5.75, -7.48], [-6.36, -9.53],
  [-6.33, -7.73], [-3.92, -6.23], [0.50, 3.33], [-1.36, -0.51], [-4.18, -8.28],
  [2.24, 8.07], [-7.21, -10.90], [-4.16, -5.30], [-2.67, -2.81], [-0.88, -1.59],
  [5.70, 13.57], [-6.01, -9.70], [0.28, 1.96], [1.85, 6.37], [-9.07, -14.33],
  [2.15, 11.07], [-6.59, -9.83], [-8.70, -13.88], [8.98, 20.81], [9.31, 17.79],
  [6.17, 15.28], [-3.91, -4.69], [-8.05, -8.17], [3.68, 9.98], [-1.20, 1.21],
  [-7.56, -12.19], [-0.10, 0.47], [-9.31, -13.34], [8.19, 20.88], [-4.82, -5.07],
  [3.25, 7.68], [-3.77, -1.73], [0.40, 0.99], [0.93, 6.04], [-6.30, -5.22]
]

size = len(points_array)
print(linear_Regression(points_array , size))
       
    
