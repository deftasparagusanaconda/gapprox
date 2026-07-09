#class Null:
#    'to denote the absence of something, like a placeholder; for when None is not considered as the absence of something'
#	#def __repr__():
#	#	return f"<Null() at {hex(id(self))}>"
from typing import Any, Generator, Type
from collections.abc import Sized

def get_all_attrs(obj: Any) -> Generator[str, None, None]:
	yield from getattr(obj, '__slots__', ())
	yield from getattr(obj, '__dict__', ())

def custom_repr(cls: Type):

	def new_repr(self):
		attrs: dict[str, Any] = {name: getattr(self, name) for name in get_all_attrs(self)}

		if not attrs:
			return f'<{cls.__name__} at {hex(id(self))}>'
		
		entries = []
		for name, val in attrs.items():
			if isinstance(val, Sized):
				entries.append(f'{len(val)} {name}')
			else:
				entries.append(f'{name}={val}')
		
		return f"<{cls.__name__} at {hex(id(self))}: {', '.join(entries)}>"
	
	cls.__repr__ = new_repr
	return cls


# mainly for optimizer
import queue

class DiscardingQueue(queue.Queue):
	'subclass of queue.Queue that discards older elements if queue is full'
	def put(self, item):
		'very primitive technology, but good enough for our purpose'
		# PRIMITIVE TECHNOLOGY!!!!!
		with self.mutex:
			if self.maxsize > 0 and self._qsize() >= self.maxsize:
				self._get()
			self._put(item)
			self.unfinished_tasks += 1
			self.not_empty.notify()
	
	def see(self) -> tuple[any]:
		with self.mutex:
			return tuple(self.queue)

from typing import Iterable
def count(stuff:Iterable, *, include:set|Iterable=None, exclude:set|Iterable={None}):
	'count how many things are in stuff, either including or excluding a set of things. excludes any None by default'
	if include is not None and exclude is not None:
		raise ValueError("specify either include or exclude only")
	elif include is not None:
		return sum(thing in include for thing in stuff)
	elif exclude is not None:
		return sum(thing not in exclude for thing in stuff)
	else:
		return len(stuff)
