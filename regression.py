#Author: Jeffrin Santon T
#Date: 24/03/2025
import numpy as np
from sympy import Eq , symbols
from scipy.linalg import lu_factor, lu_solve

def polynomial_regression(data_points):
    rhs_list = []
    lhs_list = []

    for i in range(len(data_points)):
        temp = []
        for j in range(len(data_points)):  
            temp.append(data_points[i][0]**j)  
        rhs_list.append(temp)
        lhs_list.append(data_points[i][1])

    rhs = np.array(rhs_list)
    lhs = np.array(lhs_list)

    lhs = lhs.reshape(-1, 1)


    lu, piv = lu_factor(rhs)

    coefficients = lu_solve((lu, piv), lhs)

    res = ""
    for i in range(len(coefficients)):
        if i == len(coefficients) -1:
            res += str(coefficients[i]) + "x^" + str(i) +"  "
            break
        res += str(coefficients[i][0]) + "x^" + str(i) + "+ "
    return res
