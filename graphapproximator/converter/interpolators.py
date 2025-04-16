'''from expressions import polynomial_regression as pr
import sympy
def find_equation(point1 , point2):
    x,y = sympy.symbol('x y')
    eq = sympy.Eq((y-point1[1])*(point2[0]-point1[0]), (point2[1]-point1[1])*(x-point1[0]))
    print(eq)
    return eq
def linear_interpolator(data_points , offset:int = 0.1):
    if(len(data_points) == 0):
        raise ValueError("Invalid Data_points")
    interpolated = []
    interpolated.append(data_points[0][1])
    
    for i in range(len(data_points)-1):
        if data_points[i+1][0] - data_points[i][0] == 0:
            continue
        if data_points[i+1][0] - data_points[i][0] > offset:
            equation = find_equation(data_points[i] , data_points[i+1])
'''
def linear(points, step):
    from math import sqrt
    # Ensure points are sorted by x-coordinate
    points = sorted(points, key=lambda p: p[0])
    
    if len(points) < 2 or step <= 0:
        return points

    result = []
    x_min, y_min = points[0]
    x_max, y_max = points[-1]

    # Number of interpolated points
    num_points = int((x_max - x_min) / step) + 1

    for i in range(num_points):
        x = x_min + i * step
        
        # Find the two points that the x falls between
        if x <= x_min:
            result.append((x_min, y_min))
        elif x >= x_max:
            result.append((x_max, y_max))
        else:
            for j in range(1, len(points)):
                x0, y0 = points[j - 1]
                x1, y1 = points[j]
                
                if x0 <= x <= x1:
                    # Linear interpolation formula
                    t = (x - x0) / (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    result.append((x, y))
                    break

    return result

def polynomial(data_points , degree:int=None):
    import numpy as np
    from ..expressions import polynomial as expr_poly
    rhs_list = []
    lhs_list = []
    if degree is None:
    	degree = len(data_points)
    
    for i in range(len(data_points)):
        temp = []
        for j in range(degree):  
            temp.append(data_points[i][0]**j)  
        lhs_list.append(temp)
        rhs_list.append(data_points[i][1])
    rhs = np.array(rhs_list)
    lhs = np.array(lhs_list)
    coefficients, *_ = np.linalg.lstsq(lhs , rhs, rcond=None)
    return expr_poly(coefficients)
    """res = ""
    for i in range(len(coefficients)):
        if i == len(coefficients) -1:
            res += str(round(coefficients[i] ,3)) + "*x^" + str(i) +"  "
            break
        res += str(round(coefficients[i],3)) + "*x^" + str(i) + "+ "
    return res
    """
