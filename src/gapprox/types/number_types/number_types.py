from abc import ABC

class Number(ABC):
	"an object representing a quantity or an idea of such. any derived class shall implement methods that preserve the type. that is to say, it should only implement operators that are closed under that number type"
	...

class ScalarNumber(Number):
	"a Number which lives on the one-dimensional real number line"
	...

class CompositeNumber(Number):
	"a Number which is composed of ScalarNumber, like a Number compound"
	...

class Hypercomplex(CompositeNumber):
	"a number that does not live on just the real number line and often has more than one scalar dimension and with special algebraic rules like imaginary units, nilpotent elements, noncommutativity, etc."
	...
