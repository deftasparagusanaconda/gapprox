# the heart of the project
# the engine only makes sense as an instance
# the instance manages your current configuration of generator, expression, interpolator, ...
# the instance also exposes a list of available modules (generators, expressions, interpolators, ...)

from .components import interpolators, generators, expressions, outliers, parser
from .components import optimizer
from .import utils

class Engine():
	# expose modules through the class instance 
	parser = parser.parser
	interpolators = interpolators
	generators = generators
	optimizers = optimizers
	expressions = expressions
	outliers = outliers
	output_types = ("values", "points", "string")

	# store configuration
	# instance variables
	def __init__(self):
		self.input = None
		self.output = None
		self.interpolator = None
		self.generator = None
		self.optimizer = None
		self.expression = None
		self.input_type = None
		self.output_type = None
		self.outliers = None
	
	#def auto():
	#	"""mini-AI to choose which approximation is best"""
	
	def approximate(self, input=None):
		"""calculate an approximation using the configuration given (in other words, start the data pipeline)"""

		# get data
		if input is None:
			if self.input:
				input = self.input
			else:
				raise ValueError("no input provided!\nuse `ga.input = someinput` or ga(someinput)")

		if self.parser:
			input = self.parser(input)
		if self.interpolator:
			input = self.interpolator(input)
		if self.generator:
			input = self.generator(input)
		if self.optimizer:
			input = self.optimizer(ga,input)
		if self.expression:
			input = self.expression(input)

		self.output = input
		return input
	__call__ = approximate	# ga() and ga.approximate() now do the same thing

	# provided for API convenience
	@staticmethod
	def line(input, output_type="string"):
		"""least squares line approximation (https://en.wikipedia.org/wiki/Linear_least_squares)
provided for convenience"""
		return expressions.polynomial.polynomial(generators.line.least_squares(input), number_of_points=len(input), output_type=output_type)
	linear = line
	
	# provided for API convenience
	#@staticmethod
	#def parabola(self, input=None):
	#	"""least squares parabola approximation"""
	#quad = quadratic = parabola
	# to be continued later :P
	
	# should this be static? or take array1 & array2?
	def show(self):
		"""plot ga.input and ga.output using matplotlib"""
		from matplotlib.pyplot import plt_plot, plt_show
		try:
			plt_plot(self.input)
		except:
			pass
		try:
			plt_plot(self.output)
		except:
			pass
		plt_show()
	plot = show
		
	# basically what you see when you do `print(ga)` in the python interpreter
	def __repr__(self):
		return f"<Engine instance & module 'graphapproximator' at {hex(id(self))}>"
		
	def new(self):			# foo = ga.new() creates new instance
		"""return a new instance of Engine"""
		return type(self)()
	
	def copy(self):			# foo = ga.copy() creates a copy
		"""returns a copy of the current Engine instance"""
		from copy import deepcopy
		return deepcopy(self)
