import scipy.fft, numpy

# returns a string, the f(x) representation of the input array as a periodic-extended fourier series for discrete input

# implement user-defined output formatting
def approx_fft(inarr):
	output = "f(x) = \n"

	n = len(inarr)	# no. of points

	coefficients = scipy.fft.fft(inarr, norm="forward")
	
	realarr = numpy.real(coefficients)
	imagarr = -numpy.imag(coefficients)	# -ve because from both eulers formula and fft output, i**2 = -1

	for i in range(n):
		output += str(realarr[i])
		output += "*cos(2*pi*" + str(i) + '/' + str(n) + "*x) + "
		output += '\t'
		output += str(imagarr[i])
		output += "*sin(2*pi*" + str(i) + '/' + str(n) + "*x) + "
		output += '\n'


	# should return a string
	return output
