from ast import parse 
def str_to_ast(expr:str):
	'parse a str expression to an ast tree'
	return parse(expr, mode='eval').body

#class Null:
#    'to denote the absence of something, like a placeholder; for when None is not considered as the absence of something'
#	#def __repr__():
#	#	return f"<Null() at {hex(id(self))}>"

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
