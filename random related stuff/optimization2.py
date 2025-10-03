# lets get serious

from typing import Iterable, Generator, Queue
import gapprox as ga
from gapprox.misc import DiscardingQueue
import random

# generates a new set of parameters to test. will implement black box optimizers like BFGS or such. many kinds will be implemented here
def predictor(history: DiscardingQueue[tuple[tuple[any], float]], log: DiscardingQueue[tuple[tuple[any], float]]) -> tuple[any]:
	return (random.random()*2, random.random()-0.5)

# higher score may not always be better. sometimes you might want to reward scores that are nearer to, say, 10. you can do that with this
def rewarder(score: float) -> float:
	return -score

def error(approximation: Sequence[any], original: Sequence[any], error: callable=ga.errors.difference_squared, collapser: callable=ga.collapsers.sum):
    'calculate how much discrepancy is between two arrays of numbers. uses RMSE (root mean squared error) by default'
    if len(original) != len(approximation):
        raise ValueError(f"length mismatch: len(original)={len(original)}, len(approximation)={len(approximation)}")

    return collapser(error(a, b) for a, b in zip(original, approximation))

original_samples: tuple[list[any]] = ([1, 2, 3], [1, 2, 3])
approx: ga.Expression = ga.Expression("a * x + b")	# a line approximation
parameters: tuple[str] = ('a','b')
variables: tuple[str] = ('x')
history_maxsize = 10

# stores previous guesses as (parameters: tuple, rewards: tuple) tuples
history: DiscardingQueue[tuple[tuple[any], tuple[float]]] = ga.DiscardingQueue(maxsize=history_maxsize)	

# stores improvements as (parameters: tuple, rewards: tuple) tuples
log: DiscardingQueue[tuple[tuple[any], tuple[float]]] = ga.DiscardingQueue(maxsize=log_maxsize)	

# stores guesses that are better in one objective but also worse in another
pareto_front: set[tuple[float]] = set()

for i in range(1000000):
	parameter_values: tuple[any] = predictor(history.see(), log.see())

	parameters_dict: dict[str, float] = dict((param, value) for param, value in zip(parameters, parameter_values))

	approximation_samples: Generator[float, None, None] = (approx(x=var_val, **parameters_dict) for var_val in original_samples[0])

	errors: Generator[float, None, None] = (ga.errors.difference_absolute(approx, original) for approx, original in zip(original_samples[0], approximation_samples))
	error: float = ga.collapsers.mean(errors)

	rewards: tuple[float] = (error,)

	
	
	history.put((parameter_values, error))

	print(parameter_values)
