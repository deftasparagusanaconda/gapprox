# a collapser takes a vector of things and collapses them into one scalar

from builtins import min
from builtins import max
from builtins import sum

def weighted_sum(things, weights):
	'sum them up with weights'

def power_sum(things, power):
	raise NotImplementedError

def weighted_power_sum(things, power, weights):
	raise NotImplementedError

from statistics import mean

def weighted_mean(things, weights):
	'arithmetic them up with weights'

def power_mean(things, power):
	raise NotImplementedError

def weighted_power_mean(things, power, weights):
	raise NotImplementedError

def product(things):
	'multiply them all. not same as summing their logarithm, because log of a negative number gives a complex number. wierd huh?? i think its cool'
	raise NotImplementedError

def weighted_product(things, weights):
	'multiply them with weights'
	raise NotImplementedError

def power_product(things, power):
	raise NotImplementedError

def weighted_power_product(things, power, weights):
	raise NotImplementedError
