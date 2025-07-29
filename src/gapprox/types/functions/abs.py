from ..number_types.natural import Natural
from ..number_types.whole import Whole

def abs(x):
	if isinstance(x, (Natural, Whole)):
		return abs(x)

