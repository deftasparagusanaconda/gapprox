def console_clear():
	print("\033[2J\033[H", end='')

def console_clear_line():
	print("\033[1A\033[K\r", end='')

def error_soft(input):
	print(input)
	# will include a update_UI() that sends a global UI update signal

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

#Author: T. Jeffrin Santon
#Date: 28/02/2025
def linear_d_approx(data_points , point_of_approx , position):
    #Slope calculation
    slope = (data_points[position + 1][1] - data_points[position - 1][1])/(data
_points[position + 1][0] - data_points[position - 1][0])
    print(slope) #debugging
    output = "y - " + str(point_of_approx[1]) + " = "  + str(slope) + "(x - " +
 str(point_of_approx[0])+ ")"
    return output

