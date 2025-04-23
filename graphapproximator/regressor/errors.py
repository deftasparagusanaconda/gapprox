# error functions take two arrays and return the error (how different they are) as single number
# these are different ways to measure how different they are

"""
# see https://en.wikipedia.org/wiki/Generalized_mean
def weighted_power_mean(num_arr, weight_arr, power = 1):
	if len(num_arr) != len(weight_arr):
		print("ERROR:\tweighted_power_mean(num_arr, weight_arr, power) got different lengths!")
		print("\tlen(num_arr)    =", len(num_arr))
		print("\tlen(weight_arr) =", len(weight_arr))
		return -1
	
	if 0 == power:					# weighted geometric mean
		error_total = abs(num_arr[0])**weight_arr[0]
		for i in range(1,len(num_arr)):
			error_total *= abs(num_arr[i])**weight_arr[i]
		return error_total**(1/sum(weight_arr))

	else:						# weighted power mean
		error_sum = 0
		for i in range(len(num_arr)):
			error = abs(num_arr[i])
			if error != 0:
				error_sum += weight_arr[i] * error**power
		
		return (error_sum/sum(weight_arr))**(1/power)
"""
# after making all this, i saw that scipy already had an implementation of weighted power mean. oh well :/
"""
def power_mean(num_arr, power = 1):
	import scipy.stats
	return _scipy.stats.pmean(num_arr, power)

def weighted_power_mean(num_arr, weight_arr, power = 1):
	import scipy.stats
	if len(num_arr) != len(weight_arr):
                print("ERROR:\tweighted_power_mean(num_arr, weight_arr, power) got different lengths!")
                print("\tlen(num_arr)    =", len(num_arr))
                print("\tlen(weight_arr) =", len(weight_arr))
                return -1

	return _scipy.stats.pmean(num_arr, power, weights=weight_arr)

def error_power_mean(arr_a, arr_b, power = 1):
	import scipy.stats
	if len(arr_a) != len(arr_b):
		print("ERROR:\terror_power_mean(arr_a, arr_b, power) got different lengths!")
		print("\tlen(arr_a) =", len(arr_a))
		print("\tlen(arr_b) =", len(arr_b))
		return -1

	arr_c = [abs(a-b) for a, b in zip(arr_a, arr_b)]
	print(arr_c)
	return _scipy.stats.pmean(arr_c, power)
"""

# https://en.wikipedia.org/wiki/Generalized_mean
def weighted_power_mean(arr_a, arr_b, weight_arr, power = 1):
	from scipy.stats import pmean
	if len(arr_a) != len(arr_b) or len(arr_a) != len(weight_arr):
		raise ValueError("error_weighted_power_mean() got different lengths")

	return pmean((abs(a-b) for a, b in zip(arr_a, arr_b)), power, weights=weight_arr)

def power_mean(arr_a, arr_b, power = 1):
	import scipy.stats
	if len(arr_a) != len(arr_b):
		raise ValueError("error_power_mean() got different lengths")

	return pmean([abs(a-b) for a, b in zip(arr_a, arr_b)], power)

# https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
def mape(arr_actual, arr_forecast):
	if len(arr_actual) != len(arr_forecast):
		raise ValueError("error_MAPE() got different lengths")

	sum = 0
	for i in range(len(arr_actual)):
		sum += abs((arr_actual[i]-arr_forecast[i])/arr_actual[i])
	return sum/len(arr_actual)

def smape(arr_actual, arr_forecast):
	if len(arr_actual) != len(arr_forecast):
		raise ValueError("error_SMAPE() got different lengths")

	sum = 0
	for i in range(len(arr_actual)):
		sum += abs(arr_forecast[i]-arr_actual[i]) / (abs(arr_actual[i])+abs(arr_forecast[i]))*2
	return sum/len(arr_actual)
"""
myarr1 = [2,4,5]
myarr2 = [4,4,4]
myweightarr = [1,1,1]
power = 1

#print(error_weighted_power_mean(myarr1, myarr2, myweightarr, power))
print(error_power_mean(myarr1, myarr2))
"""


# implement wMAPE, MASE, MDA, MAAPE
# implement Pearson correlation coefficient (PCC), Spearman rank correlation
# implement cosine similarity (from dot product)
# implement hellinger distance, KL divergence, Wasserstein distance
