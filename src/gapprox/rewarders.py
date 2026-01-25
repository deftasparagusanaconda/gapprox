# a rewarder takes some value and returns a reward. because sometimes you might want to reward the program for having lower values, like for example, minimizing complexity, or for having higher values, like for example, maximizing accuracy
# 
# a rewarder can be applied on both an objective score (the output of an objective function) and a parameter (the input of an objective function) so you arent maximizing the reward for just the outputs of the objective function. you are also maximizing the reward for the inputs. we may also thus treat both as living on the same space, as they are both rewards.
# 
# this has a nice ramification: we dont need to define constraints. the reward system *is* the constraint system. heres how:
# say you want an input parameter to be within 0 ≤ x ≤ 1
# if x is in [0, 1], you reward 0.0
# if x is not in [0, 1], you reward -∞
# 
# since the optimizer sees -∞ in its reward, it will think 'clearly -∞ cant be an improvement over anything' so it will skip the entire rest of the iteration, because it knows it has made a direly bad parameter. it will also know to avoid that next time :)

# NOTE:
# a reward of 0.0 is no effect
# a negative reward is a punishment
# a positive reward is an encouragement

def maximize(score: float) -> float:
	'reward higher scores. more is better'
	return score

def minimize(score:float) -> float:
	'reward lower scores. less is better'
	return -score

def towards(score:float, number:float) -> float:
	'reward scores nearer to a number'
	return -abs(score-number)

def away(score:float, number:float) -> float:
	'reward scores farther from a number'
	return abs(score-number)

def within(score: float, low: float = float('-inf'), high: float = float('inf'), *, reward: float = 0.0, punishment: float = float('-inf')) -> float:
	'0.0 if low ≤ score ≤ high else -∞'
	return reward if low <= score <= high else punishment


def gaussian(score:float, number:float, stdev:float) -> float:
	'reward scores near a number in a gaussian distribution'
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


