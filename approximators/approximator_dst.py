import scipy.fft

# returns a string, the f(x) representation of the input array as a DST decomposition
def approx_dst(inarr, dst_type):
	if dst_type not in [1,2,3,4]:
		return "DST type " + str(dst_type) + " is not supported"

	output = "f(x) = \n"

	n = len(inarr)	# no. of points

	coefficients = scipy.fft.dst(inarr, type=dst_type, norm="forward")
	
	if 1 == dst_type:
		output += "  2 * " + str(coefficients[0]) + " * sin(pi*(x+1)*(0+1)/(" + str(n) + "+1))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * sin(pi*(x+1)*(" + str(i) + "+1)/(" + str(n) + "+1))\n"

	elif 2 == dst_type:
		output += "  2 * " + str(coefficients[0]) + " * sin(pi*(0+1)*(2*x+1)/(2*" + str(n) + "))\n"
		for i in range(1, n-1):
			output += "+ 2 * " + str(coefficients[i]) + " * sin(pi*(" + str(i) + "+1)*(2*x+1)/(2*" + str(n) + "))\n"
		output += "+ 1 * " + str(coefficients[-1]) + " * sin(pi*(" + str(n-1) + "+1)*(2*x+1)/(2*" + str(n) + "))\n"
	elif 3 == dst_type:
		output += "  2 * " + str(coefficients[0]) + " * sin(pi*(x+1)*(2*0+1)/(2*" + str(n) + "))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * sin(pi*(x+1)*(2*" + str(i) + "+1)/(2*" + str(n) + "))\n"

	elif 4 == dst_type:
		output += "  2 * " + str(coefficients[0]) + " * sin(pi*(2*x+1)*(2*0+1)/(4*" + str(n) + "))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * sin(pi*(2*x+1)*(2*" + str(i) + "+1)/(4*" + str(n) + "))\n"

	return output

