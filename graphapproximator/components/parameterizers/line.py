#Author : T.Jeffrin Santon
#Date : 27.02.2025
def least_squares(points, output_type:str|list[str]="params"):
    summation_x ,summation_xy , summation_sqx ,summation_y = 0 , 0 , 0 , 0
    no_of_points = len(points)
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


    output = {}
    if "string" in output_type:
        output = "y = " + str(slope) + "x" + " + " + str(y_intercept) 
    if "params" in output_type:
        output["params"] = [y_intercept, slope]

    if len(output) == 1:
        return next(iter(output.values()))
    else:
        return output

# please update least_squares to support values[]
# the values[] can be assumed to be points with:
# x as index of the value
# y as the value
#
# input type will be discriminated by strings "values" and "points" (for now)
