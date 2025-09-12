# a rewarder takes an objective score and returns a reward. because sometimes you might want to reward the program for having lower scores, like for example, minimizing complexity 

def maximize(score:float) -> float:
	'reward higher scores. more is better'
	return score

def minimize(score:float) -> float:
	'reward lower scores. less is more. and more is always better hahahaha'
	return -score

def towards(score:float, number:float) -> float:
	'reward scores near a number'
	return -abs(score-number)

def away(score:float, number:float) -> float:
	'reward scores far away from number'
	return abs(score-number)

def gaussian(score:float, number:float, stdev:float) -> float:
	'reward scores near a number'
	from math import exp
	return exp(-(score-number)**2/(2*stdev**2))

def multimodal(score: float, peaks: list[float], stdevs: list[float], heights: list[float] | None = None) -> float:
	"reward scores near the given peaks, with optional peak heights"
	from math import exp

	heights = [1.0]*len(peaks) if heights is None else heights

	if not (len(peaks) == len(stdevs) and len(peaks) == len(heights)):
		raise ValueError(f"length mismatch: len(peaks)={len(peaks)}, len(stdevs)={len(stdevs)}, len(heights)={len(heights)}")


	total = sum(h * exp(-((score - p) ** 2) / (2 * s ** 2)) for p, s, h in zip(peaks, stdevs, heights))

	return total / sum(heights)  # normalise so weights act like proportions
