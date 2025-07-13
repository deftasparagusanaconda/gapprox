import numpy as np

def polynomial_regression(data_points , degree:int = 3):
    rhs_list = []
    lhs_list = []
    
    for i in range(len(data_points)):
        temp = []
        for j in range(degree):  
            temp.append(data_points[i][0]**j)  
        lhs_list.append(temp)
        rhs_list.append(data_points[i][1])
    rhs = np.array(rhs_list)
    lhs = np.array(lhs_list)
    #print(rhs)
    #print(lhs)
    coefficients, *_ = np.linalg.lstsq(lhs , rhs, rcond=None)
    return coefficients
    """
    res = ""
    for i in range(len(coefficients)):
        if i == len(coefficients) -1:
            res += str(round(coefficients[i] ,3)) + "*x**" + str(i) +"  "
            break
        res += str(round(coefficients[i],3)) + "*x**" + str(i) + "+ "
    return res
    """

#points = [[12, 34], [7, 19], [25, 5], [3, 14], [18, 29], [11, 8], [30, 21], [4, 27], [22, 17], [15, 2]]
#print(polynomial_regression(points ,8))
