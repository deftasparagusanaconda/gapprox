import re

def line_to_array(slope, intercept, x_start, x_stop, x_step):
	n = int((x_stop-x_start)/x_step + 1)	# no. of points
	x_arr = []
	y_arr = []

"""	# regex to extract coefficients. if it works it works lol
	slope
"""	
	def line(x):
		return slope*x + intercept

	for i in range(n):
		x_arr.append(x_start+x_step*i)
	
	for x in x_arr:
		y_arr.append(line(x))

	return [x_arr, y_arr]
"""
def linestr_to_array(instr,x_start, x_stop, x_step)
	n = int((x_stop-x_start)/x_step + 1)    # no. of points
        x_arr = []
        y_arr = []

	

	for i in range(n):
                x_arr.append(x_start+x_step*i)
"""
print(line_to_array(12, 0, 0.3, 0.6, 0.1))

temp = input()
