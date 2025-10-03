# its hard to figure out iterative optimization willy nilly. lets make a baby model and grow it from there

from typing import Iterable, Generator
import gapprox as ga
import random

original_samples: tuple[list] = ([1, 2, 3], [1, 2, 3])
approx: ga.Expression = ga.Expression("a * x + b")	# a line approximation
params_history: list[tuple[float]] = list()
error_history: list[float] = list()
params: tuple[str] = ('a','b')

for i in range(1000000):
	param_values: tuple[float] = (random.random()*2, random.random()-0.5)
	params_dict: dict[str, float] = dict((param, value) for param, value in zip(params, param_values))
	approx_samples: Generator[float, None, None] = (approx(x=x, **params_dict) for x in original_samples[0])

	errors: Generator[float, None, None] = (ga.errors.difference_absolute(approx, original) for approx, original in zip(original_samples[0], approx_samples))
	error: float = ga.collapsers.mean(errors)
	
	if len(error_history) != 0 and error >= error_history[-1]:
		continue
	
	# update histories
	error_history.append(error)
	params_history.append(param_values)

	print(param_values)


