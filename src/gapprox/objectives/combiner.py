# a combiner function takes a vector of rewards and collapses them into one scalar reward number

def min(rewards):
	'the least reward'
	return min(rewards)

def max(rewards):
	'the greatest reward'
	return max(rewards)

def sum(rewards):
	'sum them up'
	return sum(rewards)

def weighted_sum(rewards, weights):
	'sum them up with weights'

def power_sum(rewards, power):
	raise NotImplementedError

def weighted_power_sum(rewards, power, weights):
	raise NotImplementedError

def product(rewards):
	'multiply them all. not same as summing their logarithm, because log of a negative number gives a complex number. wierd huh?? i think its cool'
	raise NotImplementedError

def weighted_product(rewards, weights):
	'multiply them with weights'
	raise NotImplementedError

def power_product(rewards, power):
	raise NotImplementedError

def weighted_power_product(rewards, power, weights):
	raise NotImplementedError

# the product* functions are just for convenience, even though product(things) is same as exp(sum(log(thing) for thing in things))
