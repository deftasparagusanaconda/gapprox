def percentile(values, threshold=50):
	import numpy

	output = []
	threshold_percentile = numpy.percentile(values, threshold)

	for index, value in enumerate(values):
		if value >= threshold_percentile:
			output.append(index)
	
	return output

"""
from random import random
myarr1 = list(random() for i in range(10))
myarr2 = list(random() for i in range(10))

myarr1.append(100)
myarr2.append(1)

result = percentile(myarr1, threshold=80)
print(result)

for i in range(11):
	print(i, myarr1[i], myarr2[i], end='')
	if i in result:
		print(" was an outlier!")
	else:
		print()
"""
