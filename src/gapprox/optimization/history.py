from collections.abc import Collection
from abc import ABC

class StoragePolicy(ABC):
	"""base class for storage structures with truncation strategies such as sliding window, top-k, reservoir, periodic checkpoints, etc.

	max_size of -1 means 'no limit'"""
	def __init__(self, data: Collection, max_size: int = -1):
		self.data: Collection = data
		self.max_size: int = max_size
		
	@abstractmethod
	def add(self, element) -> None:
		...

	def get(self) -> Collection:
		return self.data

class SlidingWindow(StoragePolicy):
	'discard older elements in favour of newer ones'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def add(self, element) -> None:
		self.data

class TopK(StoragePolicy):
	'keep best n elements'

class RandomSampling(StoragePolicy):
	'randomly acquire data (very ambiguous for now)'
