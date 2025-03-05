import scipy.fft

# returns a string, the f(x) representation of the input array as a DCT decomposition

# implement user-defined output formatting
def approx_dct(inarr, dct_type):
	if dct_type not in [1,2,3,4]:
		return "DCT type " + str(dct_type) + " is not supported"

	output = "f(x) = \n"

	n = len(inarr)	# no. of points

	coefficients = scipy.fft.dct(inarr, type=dct_type, norm="forward")
	
	if 1 == dct_type:
		output += "  1 * " + str(coefficients[0]) + " * cos(pi*x/(" + str(n) + "-1)*0)" + '\n'
		for i in range(1, n-1):
			output += "+ 2 * " + str(coefficients[i]) + " * cos(pi*x/(" + str(n) + "-1)*" + str(i) + ')\n'
		output += "+ 1 * " + str(coefficients[-1]) + " * cos(pi*x/(" + str(n) + "-1)*" + str(n-1) + ')\n'

	elif 2 == dct_type:
		output += "  1 * " + str(coefficients[0]) + " * cos(pi*0*(2*x+1)/(2*" + str(n) + "))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * cos(pi*(2*x+1)/(2*" + str(n) + ")*" + str(i) + ")\n"

	elif 3 == dct_type:
		output += "  2 * " + str(coefficients[0]) + " * cos(pi*x*(2*0+1)/(2*" + str(n) + "))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * cos(pi*x*(2*" + str(i) + "+1)/(2*" + str(n) + "))\n"

	elif 4 == dct_type:
		output += "  2 * " + str(coefficients[0]) + " * cos(pi*(2*x+1)*(2*0+1)/(4*" + str(n) + "))\n"
		for i in range(1, n):
			output += "+ 2 * " + str(coefficients[i]) + " * cos(pi*(2*x+1)*(2*" + str(i) + "+1)/(4*" + str(n) + "))\n"

	return output

myarr = [9,9,3,5,1]

print(myarr)
print(approx_dct(myarr, 5))
