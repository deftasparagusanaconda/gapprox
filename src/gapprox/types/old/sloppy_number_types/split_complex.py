from .number_types import ScalarNumber, Hypercomplex
from ..truth_types.poly_boolean import PolyBoolean
from .irrational import Irrational

class SplitComplex(Hypercomplex):
	"a + bj where a and b are Real and j² = 1 but j != 1"
	def __init__(self, arg1:ScalarNumber, arg2:ScalarNumber):
		if not (isinstance(arg1, ScalarNumber) and isinstance(arg2, ScalarNumber)):
			raise TypeError("expected two ScalarNumber")
		self.value1 = arg1
		self.value2 = arg2

	def __pos__(self):
		return self

	def __neg__(self):
		if not hasattr(self.value1, '__neg__'):
			raise TypeError(f'{self.value1} does not support negation')
		elif not hasattr(self.value2, '__neg__'):
			raise TypeError(f'{self.value2} does not support negation')
		else:
			return SplitComplex(-self.value1, -self.value2)

	def __lt__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __le__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __eq__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1==other.value1, self.value2==other.value2)

	def __ne__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1!=other.value1, self.value2!=other.value2)

	def __ge__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1>=other.value1, self.value2>=other.value2)

	def __gt__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		return PolyBoolean(self.value1>other.value1, self.value2>other.value2)

	def __add__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		elif type(self.value1)!=type(other.value1) or type(self.value2)!=type(other.value2):
			return NotImplemented
		elif isinstance(self.value1, Irrational) or isinstance(self.value2, Irrational):
			return NotImplemented
		else:
			return SplitComplex(self.value1+other.value1, self.value2+other.value2)
			# (a+c)+(b+d)j
	
	def __mul__(self, other):
		if not isinstance(other, SplitComplex):
			return NotImplemented
		elif len({type(self.value1), type(self.value2), type(other.value1), type(other.value2)}) != 1:
			return NotImplemented
		elif isinstance(self.value1, Irrational):
			return NotImplemented
		else:
			return SplitComplex(self.value1*other.value1+self.value2*other.value2, self.value1*other.value2+self.value2*other.value2)
			# (ac+bd)+(ad+bc)j
	
	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}j)"
	
	def __repr__(self):
		return f"<gapprox.SplitComplex({self.value1!r}, {self.value2!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2))

