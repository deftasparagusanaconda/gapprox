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
