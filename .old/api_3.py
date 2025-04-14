from . import interpolators, generators, expressions, outliers, parser, plotters
from .optimizer.optimizer import Optimizer
from .optimizer import strategies

class _api():
	# expose modules through the class instance
	parser = parser.parser
	interpolators = interpolators
	generators = generators
	optimizers = strategies		# ga.optimizer = something only sets its strategy
	expressions = expressions
	outliers = outliers
	output_types = ["values", "points", "string"]
	
	# store configuration
	# instance variables
	def __init__(self):
		print("__init__", self)
		self.input = None
		self.input_type = None
		self.output = None
		self.output_type = None
		
		self.interpolator = None
		self.generator = None
		self.optimizer = Optimizer()	# start instance/module hybrid
		self.expression = None
		self.plotter = plotters.matplotlib
	reset = __init__	# ga.reset() now resets the instance
	
	# THE PIPELINE!!!! -----------------------------------------------------
	def approximate(self, input=None):
		# input=None is kept for convenience-sake because
		# ga.approximate(something) is easier than
		# ga.input = something; ga.approximate()
		"""calculate an approximation using the configuration given (in other words, start the data pipeline)"""
		if input is not None:
			self.input = input
		temp = self.input
		
		temp = parser.parser(temp)	# string to func
		temp = self.interpolator(temp)	# points to points
		temp = self.generator(temp)	# points to params
		temp = self.optimizer(self, temp, self.input, self.expression)	# params to params
		temp = self.expression(temp)	# params to any
		self.output = temp

		return temp
	# the end ~w~ ----------------------------------------------------------
	__call__ = approximate	# ga() and ga.approximate() are now same
	
	# provided for convenience, so you can do ga.line(something)
	@staticmethod
	def line(input, output_type="string"):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)
provided for convenience"""
		return expressions.polynomial(generators.line.least_squares(input), number_of_points=len(input), output_type=output_type)
	
	def plot(self):
		plot(plotters(self.input, self.output))
                
	def show(self):
		"""print current configuration"""
		print("input =", self.input)
		print("input_type =", self.input_type)
		print("interpolator =", self.interpolator)
		print("generator =", self.generator)
		print("optimizer =", self.optimizer.strategy)
		print("expression =", self.expression)
		print("output =", self.output)
		print("output_type =", self.output_type)
	
	def show_full(self):
		"""print current configuration + ALL sub-configurations"""
		self.show()
		print()
		print("optimizer:")
		self.optimizer.show_full()

	# basically what you see when you do `print(ga)` in the python interpreter
	def __repr__(self):
		return f"<api instance & module 'graphapproximator' at {hex(id(self))}>"
		
	def new(self):			# foo = ga.new() creates new instance
		"""return a new instance of Engine"""
		return type(self)()

	def copy(self):			# foo = ga.copy() creates a copy
		"""returns a copy of the current Engine instance"""
		from copy import deepcopy
		return deepcopy(self)
	
api = _api()	# import api now imports an instance, not the class
	
# ideally, API should not have any static methods
