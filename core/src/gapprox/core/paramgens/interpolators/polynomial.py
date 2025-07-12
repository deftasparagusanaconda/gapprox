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

