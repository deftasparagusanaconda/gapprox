def percentile(actual, forecast, threshold=50):
	import numpy

	output = []
	diff_abs = tuple(abs(a-b) for a,b in zip(forecast, actual))
	threshold_percentile = numpy.percentile(diff_abs, threshold)

	for index, value in enumerate(diff_abs):
		if value >= threshold_percentile:
			output.append(index)
	
	return output

"""

from random import random
myarr1 = list(random() for i in range(10))
myarr2 = list(random() for i in range(10))

myarr1.append(100)
myarr2.append(1)

result = percentile(myarr1, myarr2, threshold=0.99)
print(result)

for i in range(11):
	print(i, myarr1[i], myarr2[i], end='')
	if i in result:
		print(" was an outlier!")
	else:
		print()
"""
