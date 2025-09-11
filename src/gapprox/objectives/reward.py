# a reward function takes an objective score and returns a reward

def maximize(score:float) -> float:
	return score

def minimize(score:float) -> float:
	return -score

def towards(score:float, number:float) -> float:
	'towards an exact number'
	return score-number if score < number else number-score

def away(score:float, number:float) -> float:
	'away from an exact number'
	return score-number if score > number else number-score

def roughly(score:float, number:float) -> float:
	'when you want something roughly in this neighbourhood'
	# return a parabola centred around number
	# or a gaussian distribution, i guess
	raise NotImplementedError

def bimodal(score:float, peak1:float, peak2:float) -> float:
	'when you want something either high or low'
	# return a bimodal distribution, however you want to model that
	raise NotImplementedError
