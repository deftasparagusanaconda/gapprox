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

function = input("Enter the function (in terms of x): ")
pointOfArrox = input("Enter the point of approx :")
#Detla refers to the
delta = float(input("Enter the delta :"))
if delta == 0:
    print("Not Valid")
print("The function of line is : ")

print(linear_approx(function, float(pointOfArrox) , delta))

