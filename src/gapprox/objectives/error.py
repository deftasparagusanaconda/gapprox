from .. import losses, reductions

def error(original:list[any], approximation:list[any], loss:callable=losses.difference_squared, reduction:callable=reductions.sum):
	'calculate how much discrepancy is between two arrays of numbers. uses RMSE (root mean squared error) by default'
	if len(original) != len(approximation):
		raise ValueError(f"length mismatch: len(original)={len(original)}, len(approximation)={len(approximation)}")

	return reduction(loss(a, b) for a, b in zip(original, approximation))

# error is pretty hard to find, because gapprox currently does it using discretely and numerically. and even then, it can do it by either taking in a bunch of points or taking a callable and sampling it on the spot. and gapprox should also be able to find error symbolically, continuously, analytically.

# at least im sure about one thing: error should not sample the callable inside it. it should take sampled points. because when error is evaluated for each iteration, it should not have to resample for every iteration.
