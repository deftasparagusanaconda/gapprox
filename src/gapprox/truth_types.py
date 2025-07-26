from abc import ABC

class Truth(ABC):
	"an object of logical truth"
	...

class AtomicTruth(Truth):
	"a Truth which cannot be structurally broken down further, like a Truth atom"
	...

class CompositeTruth(Truth):
	"a Truth which is composed of AtomicTruth, like a Truth compound"
	...

class Boolean(AtomicTruth):
	"an AtomicTruth denoting no/yes, false/true, off/on, F/T, 0/1, down/up, open/closed, etc."
	def __init__(self, value):
		self.value = value

class FuzzyTruth(AtomicTruth):
	"a fuzzy truth value denoting something between or beyond False/True"
	def __init__(self, value):
		self.value = value

class Polyboolean(CompositeTruth):
	"a Truth representing an ordered collection of Boolean"
	def __init__(self, *args):
		self.values = tuple(value for value in args if isinstance(value, Boolean))
	
	def __iter__(self):    # i want to mark that a Polyboolean is an iterable
		return iter(self.values)

class PolyFuzzyTruth(CompositeTruth):
	"a Truth representing an ordered collection of FuzzyTruth"
	def __init__(self, *args):
		self.values = tuple(value for value in args if isinstance(value, FuzzyTruth))
	
	def __iter__(self):
		return iter(self.values)
