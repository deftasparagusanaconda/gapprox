from .number_types import ScalarNumber, Hypercomplex
from ..truth_types.poly_boolean import PolyBoolean
from .irrational import Irrational
from .imaginary import Imaginary

class Complex(Hypercomplex):
	"a + bi where a and b are Real and i² is -1"
	def __init__(self, arg1, arg2):
		if isinstance(arg1, ScalarNumber) and isinstance(arg2, ScalarNumber):
			self.value1 = arg1
			self.value2 = arg2

		elif isinstance(arg1, ScalarNumber) and isinstance(arg2, Imaginary):
			self.value1 = arg1
			self.value2 = arg2.value

		elif isinstance(arg1, Imaginary) and isinstance(arg2, ScalarNumber):
			self.value1 = arg2
			self.value2 = arg1.value

		else:
			raise TypeError("expected two ScalarNumber or one ScalarNumber and one Imaginary")

	def __lt__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __le__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __eq__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1==other.value1, self.value2==other.value2)

	def __ne__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1!=other.value1, self.value2!=other.value2)

	def __ge__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<=other.value1, self.value2<=other.value2)

	def __gt__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		return PolyBoolean(self.value1<other.value1, self.value2<other.value2)

	def __add__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		elif type(self.value1)!=type(other.value1) or type(self.value2)!=type(other.value2):
			return NotImplemented
		elif isinstance(self.value1, Irrational) or isinstance(self.value2, Irrational):
			return NotImplemented
		else:
			return Complex(self.value1+other.value1, self.value2+other.value2)
			# (a+c)+(b+d)i

	def __mul__(self, other):
		if not isinstance(other, Complex):
			return NotImplemented
		elif len({type(self.value1), type(self.value2), type(other.value1), type(other.value2)}) != 1:
			return NotImplemented
		elif isinstance(self.value1, Irrational):
			return NotImplemented
		else:
			return Complex(self.value1*other.value1-self.value2*other.value2, self.value1*other.value2+self.value2*other.value2)
			# (ac-bd)+(ad+bc)i

	def __complex__(self):
		return complex(float(self.value1), float(self.value2))

	def __str__(self):
		return f"({self.value1}{'' if float(self.value2)<0 else '+'}{self.value2}i)"
	
	def __repr__(self):
		return f"<gapprox.Complex({self.value1!r}, {self.value2!r})>"

	def __hash__(self):
		return hash((self.value1, self.value2))
